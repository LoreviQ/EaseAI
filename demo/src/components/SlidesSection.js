const SlidesSection = ({ slides }) => {
  if (!slides || slides.length === 0) return null;
  
  return (
    <div className="w-96 bg-dark-tertiary border border-border rounded-lg flex flex-col">
      <div className="p-4 border-b border-border">
        <h3 className="font-medium text-text-primary">Generated Slides ({slides.length})</h3>
      </div>
      
      <div className="flex-1 p-5 overflow-y-auto space-y-4">
        {slides.map((slide, index) => (
          <div key={index} className="bg-border rounded-md p-4">
            <div className="font-medium text-text-primary mb-2">
              {slide.slide_number}. {slide.title}
            </div>
            <div className="text-xs text-text-secondary mb-2">
              {slide.description}
            </div>
            <div className="text-sm text-text-primary">
              {slide.content}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SlidesSection;