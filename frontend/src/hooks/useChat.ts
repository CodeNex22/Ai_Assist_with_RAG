import { useMutation, useQuery } from '@tanstack/react-query';
import { getHealth, getModels, sendChatMessage, uploadDocuments } from '../api/client';

export function useHealth() {
  return useQuery({ queryKey: ['health'], queryFn: getHealth });
}

export function useModels() {
  return useQuery({ queryKey: ['models'], queryFn: getModels });
}

export function useSendMessage() {
  return useMutation({ mutationFn: ({ message, chatId }: { message: string; chatId?: string }) => sendChatMessage(message, chatId) });
}

export function useUploadDocuments() {
  return useMutation({ mutationFn: (file: File) => uploadDocuments(file) });
}
