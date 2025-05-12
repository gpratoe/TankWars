import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default ({mode}) => {
  
  const env = loadEnv(mode, process.cwd());
  console.log('BASE URL:', env.VITE_BASE_URL);
  
  return defineConfig({
    plugins: [react()],
    base: env.VITE_BASE_URL || '/',
  });

}