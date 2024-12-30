from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Note, NoteGroup
from .serializers import NoteSerializer, NoteGroupSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta, date
from django.db.models.functions import TruncDate, TruncMonth
from django.db.models import Q

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class NoteGroupViewSet(viewsets.ModelViewSet):
    serializer_class = NoteGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # 管理员可以看到所有分组
        if user.role == 'admin':
            return NoteGroup.objects.all()
        
        # 普通用户只能看到自己创建的和被授权的分组
        return NoteGroup.objects.filter(
            Q(creator=user) |  # 用户创建的分组
            Q(note_group_users=user)  # 用户被授权的分组
        ).distinct()

    def perform_create(self, serializer):
        # 创建分组时，同时添加到用户的授权分组中
        group = serializer.save(creator=self.request.user)
        self.request.user.note_group.add(group)


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = [
        'group__id', 'group__name', 'creator__id', 'creator__username'
    ]
    search_fields = [
        'title', 'content', 'group__id', 'group__name', 'creator__id', 'creator__username'
    ]

    def get_queryset(self):
        user = self.request.user
        
        # 如果是管理员，返回所有笔记
        if user.role == 'admin':
            return Note.objects.all()
        
        # 构建查询条件
        queryset = Note.objects.filter(
            Q(creator=user) |  # 用户创建的笔记
            Q(note_users=user) |  # 用户被直接授权的笔记
            Q(group__note_group_users=user)  # 用户被授权的分组中的笔记
        ).distinct()
        
        # 应用分组过滤
        group_id = self.request.query_params.get('group_id', None)
        if group_id is not None:
            queryset = queryset.filter(group_id=group_id)
            
        return queryset

    def perform_create(self, serializer):
        # 创建笔记时，同时添加到用户的授权笔记中
        note = serializer.save(creator=self.request.user)
        self.request.user.note.add(note)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        user = request.user
        time_range = request.query_params.get('range', 'week')
        today = timezone.now().date()
        
        # 根据用户角色获取笔记查询集
        if user.role == 'admin':
            notes_queryset = Note.objects.all()
            groups_queryset = NoteGroup.objects.all()
        else:
            notes_queryset = Note.objects.filter(
                Q(creator=user) |
                Q(note_users=user)
            ).distinct()
            groups_queryset = NoteGroup.objects.filter(
                Q(creator=user) |
                Q(note_group_users=user)
            ).distinct()
        
        # 获取基础统计数据
        total_notes = notes_queryset.count()
        total_groups = groups_queryset.count()
        
        # 获取分组分布数据
        groups_distribution = (
            Note.objects
            .filter(creator=request.user)
            .values('group__name')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        # 处理没有分组的笔记
        groups_data = []
        ungrouped_notes = 0
        for item in groups_distribution:
            if item['group__name'] is None:
                ungrouped_notes = item['count']
            else:
                groups_data.append({
                    'name': item['group__name'],
                    'value': item['count']
                })
        
        # 如果有未分组的笔记，添加到列表中
        if ungrouped_notes > 0:
            groups_data.append({
                'name': '未分组',
                'value': ungrouped_notes
            })
        
        # 根据时间范围获取趋势数据
        if time_range == 'year':
            # 获取最近12个月的数据
            start_date = today - timedelta(days=365)
            notes_trend = (
                Note.objects
                .filter(
                    creator=request.user,
                    created_at__date__gte=start_date,
                    created_at__date__lte=today
                )
                .annotate(month=TruncMonth('created_at'))
                .values('month')
                .annotate(count=Count('id'))
                .order_by('month')
            )
            
            # 生成所有月份的数据
            date_counts = {}
            current_date = date(start_date.year, start_date.month, 1)  # 使用每月1号
            end_date = date(today.year, today.month, 1)
            
            while current_date <= end_date:
                date_counts[current_date.strftime('%Y-%m')] = 0
                # 移动到下个月的1号
                if current_date.month == 12:
                    current_date = date(current_date.year + 1, 1, 1)
                else:
                    current_date = date(current_date.year, current_date.month + 1, 1)
            
            # 填充实际数据
            for entry in notes_trend:
                date_counts[entry['month'].strftime('%Y-%m')] = entry['count']
                
        elif time_range == 'month':
            # 获取最近30天的数据
            start_date = today - timedelta(days=29)
            notes_trend = (
                Note.objects
                .filter(
                    creator=request.user,
                    created_at__date__gte=start_date,
                    created_at__date__lte=today
                )
                .annotate(date=TruncDate('created_at'))
                .values('date')
                .annotate(count=Count('id'))
                .order_by('date')
            )
            
            # 生成所有日期的数据
            date_counts = {
                (start_date + timedelta(days=i)).strftime('%Y-%m-%d'): 0 
                for i in range(30)
            }
            
            # 填充实际数据
            for entry in notes_trend:
                date_counts[entry['date'].strftime('%Y-%m-%d')] = entry['count']
                
        else:  # 默认按周统计
            # 获取最近7天的数据
            start_date = today - timedelta(days=6)
            notes_trend = (
                Note.objects
                .filter(
                    creator=request.user,
                    created_at__date__gte=start_date,
                    created_at__date__lte=today
                )
                .annotate(date=TruncDate('created_at'))
                .values('date')
                .annotate(count=Count('id'))
                .order_by('date')
            )
            
            # 生成所有日期的数据
            date_counts = {
                (start_date + timedelta(days=i)).strftime('%Y-%m-%d'): 0 
                for i in range(7)
            }
            
            # 填充实际数据
            for entry in notes_trend:
                date_counts[entry['date'].strftime('%Y-%m-%d')] = entry['count']
        
        return Response({
            'total_notes': total_notes,
            'total_groups': total_groups,
            'notes_charts': [
                {'date': date, 'count': count}
                for date, count in date_counts.items()
            ],
            'groups_distribution': groups_data  # 添加分组分布数据
        })
