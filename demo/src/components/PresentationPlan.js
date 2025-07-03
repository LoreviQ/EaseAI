const PresentationPlan = ({ plan, projectId, loading, setLoading, setError, setProjectPhase, onPlanApproved }) => {
  const API_BASE = 'http://localhost:8000/v1';
  
  const approvePlan = async () => {
    if (!projectId || !plan) return;
    
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${API_BASE}/projects/${projectId}/plan/approve`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to approve plan');
      }
      
      setProjectPhase('generation');
      onPlanApproved();
      
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  if (!plan) return null;
  
  return (
    <div className="w-96 bg-dark-tertiary border border-border rounded-lg flex flex-col">
      <div className="p-4 border-b border-border">
        <h3 className="font-medium text-text-primary">Presentation Plan</h3>
      </div>
      
      <div className="flex-1 p-5 overflow-y-auto space-y-4">
        <div>
          <label className="block text-xs text-text-secondary uppercase mb-1">Title</label>
          <div className="text-text-primary text-sm">{plan.title}</div>
        </div>
        
        <div>
          <label className="block text-xs text-text-secondary uppercase mb-1">Objective</label>
          <div className="text-text-primary text-sm">{plan.objective}</div>
        </div>
        
        <div>
          <label className="block text-xs text-text-secondary uppercase mb-1">Target Audience</label>
          <div className="text-text-primary text-sm">{plan.target_audience}</div>
        </div>
        
        <div>
          <label className="block text-xs text-text-secondary uppercase mb-1">Tone</label>
          <div className="text-text-primary text-sm">{plan.tone}</div>
        </div>
        
        <div>
          <label className="block text-xs text-text-secondary uppercase mb-1">Duration</label>
          <div className="text-text-primary text-sm">{plan.duration} minutes</div>
        </div>
        
        {plan.research_summary && (
          <div>
            <label className="block text-xs text-text-secondary uppercase mb-1">Research Summary</label>
            <div className="text-text-primary text-sm">{plan.research_summary}</div>
          </div>
        )}
      </div>
      
      <div className="p-5">
        <button
          onClick={approvePlan}
          disabled={loading}
          className="w-full bg-accent text-black px-5 py-3 rounded-md hover:bg-accent-hover disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
        >
          {loading ? 'Approving...' : 'Approve Plan'}
        </button>
      </div>
    </div>
  );
};

export default PresentationPlan;