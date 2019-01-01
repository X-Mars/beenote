import request from '@/utils/request'

export function getNote() {
  return request({
    url: '/api-v1/note/?format=json',
    method: 'get'
  })
}

export function createNote(data) {
  return request({
    url: '/api-v1/note/?format=json',
    method: 'post',
    data
  })
}


export function getNoteById(noteId) {
  return request({
    url: '/api-v1/note/' + noteId + '?format=json',
    method: 'get'
  })
}

export function getNoteBook() {
  return request({
    url: '/api-v1/notebook/?format=json',
    method: 'get'
  })
}

export function getNoteBookBase() {
  return request({
    url: '/api-v1/notebook/?type=base&format=json',
    method: 'get'
  })
}

export function getNoteBookById(notebookId) {
  return request({
    url: '/api-v1/notebook/' + notebookId + '/?format=json',
    method: 'get'
  })
}

export function saveNoteById(noteId, data) {
  return request({
    url: '/api-v1/note/' + noteId + '/',
    method: 'patch',
    data
  })
}