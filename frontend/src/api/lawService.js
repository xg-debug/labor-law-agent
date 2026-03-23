import client from './client'

export const healthCheck = async () => {
  const { data } = await client.get('/health')
  return data
}

export const askQuestion = async (payload) => {
  const { data } = await client.post('/api/chat/ask', payload)
  return data
}

export const reviewContract = async (payload) => {
  const { data } = await client.post('/api/contract/review', payload)
  return data
}

export const generateDocument = async (payload) => {
  const { data } = await client.post('/api/document/generate', payload)
  return data
}
