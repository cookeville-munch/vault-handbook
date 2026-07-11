import { definePlugin } from '@opencode-ai/plugin'

export default definePlugin({
  name: 'retry-plugin',
  version: '1.0.0',
  hooks: {
    'model:request': async ({ model, request, retry }, next) => {
      const maxRetries = 3
      const baseDelay = 1000 // 1 second

      for (let attempt = 0; attempt <= maxRetries; attempt++) {
        try {
          return await next({ model, request })
        } catch (error) {
          if (attempt === maxRetries) throw error

          const isRetryable = error instanceof Error && 
            (error.name === 'TimeoutError' || 
             error.message.includes('timeout') ||
             error.message.includes('ECONNRESET') ||
             error.message.includes('ETIMEDOUT') ||
             (error as any).status === 429 ||
             (error as any).status >= 500)

          if (!isRetryable) throw error

          const delay = baseDelay * Math.pow(2, attempt) + Math.random() * 1000
          await new Promise(resolve => setTimeout(resolve, delay))
        }
      }
    }
  }
})