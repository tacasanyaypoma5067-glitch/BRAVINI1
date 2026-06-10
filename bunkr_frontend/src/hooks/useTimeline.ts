import { useState, useEffect } from 'react';
import { timelineService, TimelineItem, OnThisDayResponse } from '../services/timeline';

export const useTimeline = () => {
  const [timelineItems, setTimelineItems] = useState<TimelineItem[]>([]);
  const [onThisDay, setOnThisDay] = useState<OnThisDayResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadTimeline = async (page: number = 1, limit: number = 20) => {
    setIsLoading(true);
    setError(null);
    try {
      const items = await timelineService.getTimeline(page, limit);
      setTimelineItems(prev => page === 1 ? items : [...prev, ...items]);
      return items;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al cargar el timeline');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const addNote = async (content: string, tags?: number[], location?: string) => {
    try {
      const newNote = await timelineService.createNote(content, tags, location);
      setTimelineItems(prev => [newNote, ...prev]);
      return newNote;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al crear la nota');
      throw err;
    }
  };

  const loadOnThisDay = async () => {
    try {
      const data = await timelineService.getOnThisDay();
      setOnThisDay(data);
      return data;
    } catch (err: any) {
      console.error('Error loading on this day:', err);
    }
  };

  useEffect(() => {
    loadTimeline();
    loadOnThisDay();
  }, []);

  return {
    timelineItems,
    onThisDay,
    isLoading,
    error,
    loadTimeline,
    addNote,
    loadOnThisDay,
  };
};
