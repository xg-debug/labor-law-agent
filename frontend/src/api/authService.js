import client from './client'

export const loginApi = async (payload) => {
  const { data } = await client.post('/api/auth/login', payload)
  return data
}

export const registerApi = async (payload) => {
  const { data } = await client.post('/api/auth/register', payload)
  return data
}

export const meApi = async () => {
  const { data } = await client.get('/api/auth/me')
  return data
}
