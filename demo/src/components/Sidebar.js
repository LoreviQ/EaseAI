const Sidebar = ({ projectId, projectPhase }) => {
  const getPhaseStatus = (phase) => {
    switch (phase) {
      case 'research': return 'Research Phase';
      case 'planning': return 'Planning Phase';
      case 'generation': return 'Generating Content';
      case 'completed': return 'Completed';
      default: return 'Unknown Phase';
    }
  };

  const getPhaseColor = (phase) => {
    switch (phase) {
      case 'research': return 'bg-orange-500';
      case 'planning': return 'bg-blue-500';
      case 'generation': return 'bg-green-500';
      case 'completed': return 'bg-accent';
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className="w-80 bg-dark-tertiary border-r border-border p-5 overflow-y-auto">
      <div className="flex items-center gap-3 mb-8">
        <div className="w-8 h-8 bg-gradient-to-br from-accent to-primary rounded-full flex items-center justify-center text-white font-bold text-sm">
          EA
        </div>
        <h2 className="text-xl font-semibold text-text-primary">EaseAI</h2>
      </div>
      
      <div>
        <h3 className="text-lg font-medium text-text-primary mb-4">Project Status</h3>
        {projectId && (
          <div className="space-y-2">
            <div className="flex items-center">
              <div className={`w-2 h-2 rounded-full mr-2 ${getPhaseColor(projectPhase)}`}></div>
              <span className="text-text-primary">{getPhaseStatus(projectPhase)}</span>
            </div>
            <div className="text-xs text-text-secondary">
              Project ID: {projectId.slice(0, 8)}...
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;