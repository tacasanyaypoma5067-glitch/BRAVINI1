import { motion } from 'framer-motion';

interface FoxIconProps {
  size?: number;
  className?: string;
}

export const FoxIcon = ({ size = 64, className = '' }: FoxIconProps) => {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Fox Head - Embroidery Style */}
      <motion.g
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        {/* Ears */}
        <path
          d="M25 35 L35 15 L45 35 Z"
          fill="currentColor"
          opacity="0.9"
        />
        <path
          d="M55 35 L65 15 L75 35 Z"
          fill="currentColor"
          opacity="0.9"
        />
        
        {/* Inner Ears - Embroidery Detail */}
        <path
          d="M30 33 L35 20 L40 33 Z"
          fill="#E8E8ED"
          opacity="0.6"
        />
        <path
          d="M60 33 L65 20 L70 33 Z"
          fill="#E8E8ED"
          opacity="0.6"
        />

        {/* Face Shape */}
        <ellipse
          cx="50"
          cy="55"
          rx="30"
          ry="25"
          fill="currentColor"
          opacity="0.95"
        />

        {/* Snout - Lighter Area */}
        <ellipse
          cx="50"
          cy="62"
          rx="12"
          ry="10"
          fill="#E8E8ED"
          opacity="0.3"
        />

        {/* Nose */}
        <circle
          cx="50"
          cy="58"
          r="4"
          fill="#E8E8ED"
        />

        {/* Eyes - Simple Dots */}
        <circle
          cx="40"
          cy="50"
          r="3"
          fill="#E8E8ED"
        />
        <circle
          cx="60"
          cy="50"
          r="3"
          fill="#E8E8ED"
        />

        {/* Embroidery Stitch Lines - Decorative */}
        <path
          d="M35 45 Q50 40 65 45"
          stroke="currentColor"
          strokeWidth="1"
          fill="none"
          opacity="0.5"
          strokeDasharray="3,2"
        />
        
        {/* Whiskers - Subtle Lines */}
        <line
          x1="30"
          y1="60"
          x2="20"
          y2="58"
          stroke="currentColor"
          strokeWidth="0.5"
          opacity="0.4"
        />
        <line
          x1="30"
          y1="62"
          x2="20"
          y2="62"
          stroke="currentColor"
          strokeWidth="0.5"
          opacity="0.4"
        />
        <line
          x1="70"
          y1="60"
          x2="80"
          y2="58"
          stroke="currentColor"
          strokeWidth="0.5"
          opacity="0.4"
        />
        <line
          x1="70"
          y1="62"
          x2="80"
          y2="62"
          stroke="currentColor"
          strokeWidth="0.5"
          opacity="0.4"
        />
      </motion.g>
    </svg>
  );
};

export default FoxIcon;
