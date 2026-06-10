import { motion } from 'framer-motion';
import { FileText, Image, Tag, MapPin } from 'lucide-react';
import { TimelineItem } from '../services/timeline';

interface TimelineCardProps {
  item: TimelineItem;
}

const TimelineCard = ({ item }: TimelineCardProps) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('es-ES', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="bg-nordic-dark rounded-xl p-5 border border-nordic-gray hover:border-nordic-accent/30 transition-colors"
    >
      {/* Header - Type Icon + Date */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          {item.type === 'note' ? (
            <div className="w-8 h-8 rounded-lg bg-nordic-accent/20 flex items-center justify-center text-nordic-accent">
              <FileText size={16} />
            </div>
          ) : (
            <div className="w-8 h-8 rounded-lg bg-nordic-accent/20 flex items-center justify-center text-nordic-accent">
              <Image size={16} />
            </div>
          )}
          <span className="text-xs text-nordic-muted uppercase tracking-wider">
            {item.type === 'note' ? 'Nota' : 'Archivo'}
          </span>
        </div>
        <span className="text-xs text-nordic-muted">
          {formatDate(item.created_at)}
        </span>
      </div>

      {/* Content */}
      {item.type === 'note' ? (
        <p className="text-nordic-text leading-relaxed whitespace-pre-wrap">
          {item.content}
        </p>
      ) : (
        <div className="space-y-2">
          {item.file_path && (
            <div className="aspect-video bg-nordic-gray rounded-lg overflow-hidden">
              {item.file_type?.startsWith('image/') ? (
                <img
                  src={item.file_path}
                  alt={item.title || 'Archivo'}
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-nordic-muted">
                  <FileText size={32} />
                  <span className="ml-2 text-sm">{item.file_type}</span>
                </div>
              )}
            </div>
          )}
          {(item.title || item.description) && (
            <div>
              {item.title && (
                <h3 className="text-nordic-text font-medium">{item.title}</h3>
              )}
              {item.description && (
                <p className="text-nordic-muted text-sm mt-1">{item.description}</p>
              )}
            </div>
          )}
        </div>
      )}

      {/* Footer - Tags + Location */}
      {(item.tags?.length || item.location) && (
        <div className="flex items-center gap-3 mt-4 pt-4 border-t border-nordic-gray">
          {item.tags && item.tags.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {item.tags.map((tag) => (
                <span
                  key={tag.id}
                  className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs"
                  style={{
                    backgroundColor: `${tag.color}20`,
                    color: tag.color
                  }}
                >
                  <Tag size={10} />
                  {tag.name}
                </span>
              ))}
            </div>
          )}
          
          {item.location && (
            <div className="flex items-center gap-1 text-nordic-muted text-xs ml-auto">
              <MapPin size={12} />
              {item.location}
            </div>
          )}
        </div>
      )}
    </motion.div>
  );
};

export default TimelineCard;
