import React from 'react';

interface ArtemisLogoProps {
  className?: string;
}

const ArtemisLogo: React.FC<ArtemisLogoProps> = ({ className = "h-10 w-auto" }) => {
  return (
    <div className="flex items-center space-x-3 rtl:space-x-reverse">
       <svg className={className} viewBox="0 0 130 110" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="a-grad" x1="0.5" y1="0" x2="0.5" y2="1">
                <stop offset="0%" stopColor="#8A8A8A"/>
                <stop offset="100%" stopColor="#5A5A5A"/>
            </linearGradient>
            <radialGradient id="sphere-grad" cx="0.35" cy="0.35" r="0.65">
                <stop offset="0%" stopColor="#E2E8F0"/>
                <stop offset="100%" stopColor="#A0AEC0"/>
            </radialGradient>
            <linearGradient id="red-swoosh-grad" x1="0" y1="0.5" x2="1" y2="0.5">
                <stop offset="0%" stopColor="#E53E3E"/>
                <stop offset="100%" stopColor="#9B2C2C"/>
            </linearGradient>
            <linearGradient id="blue-swoosh-grad" x1="0" y1="0.5" x2="1" y2="0.5">
                <stop offset="0%" stopColor="#4299E1"/>
                <stop offset="100%" stopColor="#2B6CB0"/>
            </linearGradient>
        </defs>
        
        {/* Blue swoosh */}
        <path d="M15 95 C 40 115, 90 115, 115 95" stroke="url(#blue-swoosh-grad)" strokeWidth="14" strokeLinecap="round"/>
        
        {/* Main 'A' shape */}
        <path d="M65 8 L 115 100 L 85 100 L 65 50 L 45 100 L 15 100 Z" fill="url(#a-grad)" />

        {/* Red swoosh - drawn after 'A' to be on top */}
        <path d="M5 65 C 50 40, 80 55, 125 75" stroke="url(#red-swoosh-grad)" strokeWidth="12" strokeLinecap="round"/>

        {/* Sphere orbit path (subtle) */}
        <path d="M118 28 A 25 25 0 1 1 100 5" stroke="#A0AEC0" strokeWidth="1" strokeOpacity="0.5" />

        {/* Sphere */}
        <circle cx="100" cy="20" r="14" fill="url(#sphere-grad)" stroke="#4A5568" strokeWidth="1"/>

      </svg>
      <span className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">
        Artemis
      </span>
    </div>
  );
};

export default ArtemisLogo;
