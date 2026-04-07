import { apiRequest } from './api';

export type CommonHealthResponse = {
  status: 'ok' | string;
};

export async function getCommonHealth(): Promise<CommonHealthResponse> {
  return apiRequest<CommonHealthResponse>('/api/v1/common/health/');
}
