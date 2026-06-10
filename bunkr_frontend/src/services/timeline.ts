import api from './api';

export interface TimelineItem {
  id: number;
  type: 'note' | 'file';
  content?: string;
  file_path?: string;
  file_type?: string;
  title?: string;
  created_at: string;
  tags?: Array<{
    id: number;
    name: string;
    color: string;
  }>;
  location?: string;
}

export interface OnThisDayResponse {
  items: TimelineItem[];
  message: string;
}

export const timelineService = {
  getTimeline: async (page: number = 1, limit: number = 20): Promise<TimelineItem[]> => {
    const response = await api.get('/timeline/', {
      params: { page, limit }
    });
    return response.data;
  },

  createNote: async (content: string, tags?: number[], location?: string) => {
    const response = await api.post('/timeline/note', {
      content,
      tag_ids: tags,
      location
    });
    return response.data;
  },

  getOnThisDay: async (): Promise<OnThisDayResponse> => {
    const response = await api.get('/timeline/on-this-day');
    return response.data;
  }
};
