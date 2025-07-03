import React, { useState, useEffect } from 'react';

const SlideViewer = ({ slides }) => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [notesMinimized, setNotesMinimized] = useState(false);
  
  useEffect(() => {
    setCurrentSlide(0);
  }, [slides]);
  
  if (!slides || slides.length === 0) {
    return null;
  }
  
  const slide = slides[currentSlide];
  
  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };
  
  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };
  
  const goToSlide = (index) => {
    setCurrentSlide(index);
  };
  
  return (
    <div className="h-full flex flex-col bg-dark-tertiary border border-border rounded-lg overflow-hidden max-h-full">
      {/* Slide Header */}
      <div className="p-4 border-b border-border flex items-center justify-between bg-dark-secondary">
        <h3 className="font-medium text-text-primary">
          Slide {currentSlide + 1} of {slides.length}: {slide.title}
        </h3>
        <div className="flex items-center gap-2">
          <button
            onClick={prevSlide}
            disabled={slides.length <= 1}
            className="p-2 bg-border rounded hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed text-text-primary"
          >
            ←
          </button>
          <span className="text-text-secondary text-sm">
            {currentSlide + 1} / {slides.length}
          </span>
          <button
            onClick={nextSlide}
            disabled={slides.length <= 1}
            className="p-2 bg-border rounded hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed text-text-primary"
          >
            →
          </button>
        </div>
      </div>
      
      {/* Slide Content */}
      <div className="flex-1 flex flex-col min-h-0">
        <div className="flex-1 bg-white overflow-auto">
          <div 
            className="w-full min-h-full"
            dangerouslySetInnerHTML={{ __html: slide.content }}
          />
        </div>
        
        {/* Speaker Notes and Delivery Tutorial */}
        <div className={`${notesMinimized ? 'h-12' : 'h-48'} flex flex-col bg-dark-secondary transition-all duration-300`}>
          {/* Notes Header with Toggle */}
          <div className="flex items-center justify-between p-3 border-t border-border">
            <h4 className="font-medium text-text-primary text-sm">
              {(slide.speaker_notes || slide.delivery_tutorial) ? 'Speaker Notes & Delivery Tutorial' : 'No additional notes'}
            </h4>
            {(slide.speaker_notes || slide.delivery_tutorial) && (
              <button
                onClick={() => setNotesMinimized(!notesMinimized)}
                className="text-text-secondary hover:text-text-primary transition-colors p-1"
              >
                <svg className={`w-4 h-4 transition-transform ${notesMinimized ? 'rotate-180' : ''}`} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M6 9l6 6 6-6" />
                </svg>
              </button>
            )}
          </div>
          
          {/* Notes Content */}
          {!notesMinimized && (slide.speaker_notes || slide.delivery_tutorial) && (
            <div className="flex-1 flex min-h-0">
              {/* Speaker Notes */}
              {slide.speaker_notes && (
                <div className="flex-1 p-4 border-r border-border overflow-y-auto">
                  <h4 className="font-medium text-text-primary mb-2 text-sm">Speaker Notes</h4>
                  <div className="text-text-secondary text-sm whitespace-pre-wrap">
                    {slide.speaker_notes}
                  </div>
                </div>
              )}
              
              {/* Delivery Tutorial */}
              {slide.delivery_tutorial && (
                <div className="flex-1 p-4 overflow-y-auto">
                  <h4 className="font-medium text-text-primary mb-2 text-sm">Delivery Tutorial</h4>
                  <div className="text-text-secondary text-sm whitespace-pre-wrap">
                    {slide.delivery_tutorial}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
      
      {/* Slide Navigation */}
      <div className="p-3 border-t border-border bg-dark-secondary">
        <div className="flex gap-1 justify-center">
          {slides.map((_, index) => (
            <button
              key={index}
              onClick={() => goToSlide(index)}
              className={`w-3 h-3 rounded-full transition-colors ${
                index === currentSlide
                  ? 'bg-accent'
                  : 'bg-border hover:bg-gray-500'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default SlideViewer;