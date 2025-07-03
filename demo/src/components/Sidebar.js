const Sidebar = ({ projectId, projectPhase, projects, onSelectProject, onCreateProject, loading }) => {
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
    <div className="w-64 bg-dark-tertiary border-r border-border p-4 overflow-y-auto">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-8 h-8 bg-gradient-to-br from-accent to-primary rounded-full flex items-center justify-center text-white font-bold text-sm">
          EA
        </div>
        <h2 className="text-xl font-semibold text-text-primary">EaseAI</h2>
      </div>
      
      <div className="space-y-6">
        {/* New Project Button */}
        <button
          onClick={onCreateProject}
          disabled={loading}
          className="w-full bg-accent text-black px-4 py-3 rounded-md hover:bg-accent-hover disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium flex items-center justify-center gap-2"
        >
          {loading && (
            <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
          )}
          {loading ? 'Creating...' : '+ New Project'}
        </button>
        
        {/* Projects List */}
        <div>
          <h3 className="text-sm font-medium text-text-primary mb-3">Recent Projects</h3>
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {projects.length === 0 ? (
              <div className="text-text-secondary text-sm">No projects yet</div>
            ) : (
              projects.map((project) => (
                <div
                  key={project.id}
                  onClick={() => onSelectProject(project.id)}
                  className={`p-3 rounded-md cursor-pointer transition-colors border ${
                    projectId === project.id
                      ? 'bg-primary/10 border-primary text-text-primary'
                      : 'bg-border/50 border-transparent hover:bg-border text-text-secondary hover:text-text-primary'
                  }`}
                >
                  <div className="font-medium text-sm truncate">{project.title}</div>
                  <div className="flex items-center justify-between mt-1">
                    <div className="flex items-center gap-2">
                      <div className={`w-2 h-2 rounded-full ${getPhaseColor(project.phase)}`}></div>
                      <span className="text-xs">{getPhaseStatus(project.phase)}</span>
                    </div>
                    <div className="text-xs">
                      {new Date(project.updated_at).toLocaleDateString()}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
        
        {/* Current Project Status */}
        {projectId && (
          <div className="border-t border-border pt-4">
            <h3 className="text-sm font-medium text-text-primary mb-2">Current Status</h3>
            <div className="space-y-2">
              <div className="flex items-center">
                <div className={`w-2 h-2 rounded-full mr-2 ${getPhaseColor(projectPhase)}`}></div>
                <span className="text-text-primary text-sm">{getPhaseStatus(projectPhase)}</span>
              </div>
              <div className="text-xs text-text-secondary">
                ID: {projectId.slice(0, 8)}...
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;