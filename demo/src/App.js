import { useState } from 'react';
import Sidebar from './components/Sidebar';
import ChatSection from './components/ChatSection';
import PresentationPlan from './components/PresentationPlan';
import SlidesSection from './components/SlidesSection';

const App = () => {
  const [projectId, setProjectId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [presentationPlan, setPresentationPlan] = useState(null);
  const [slides, setSlides] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [projectPhase, setProjectPhase] = useState('research');
  
  const API_BASE = 'http://localhost:8000/v1';
  
  const createNewProject = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${API_BASE}/projects/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: 'New Presentation',
          description: 'Created from demo'
        })
      });
      
      if (!response.ok) {
        throw new Error('Failed to create project');
      }
      
      const project = await response.json();
      setProjectId(project.id);
      setMessages([]);
      setPresentationPlan(null);
      setSlides([]);
      setProjectPhase(project.phase);
      
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  const fetchSlides = async () => {
    if (!projectId) return;
    
    try {
      const response = await fetch(`${API_BASE}/projects/${projectId}/slides/`);
      
      if (response.ok) {
        const result = await response.json();
        setSlides(result.slides);
        setProjectPhase('completed');
      }
    } catch (err) {
      // Slides might not be ready yet, that's okay
    }
  };
  
  const handlePlanApproved = () => {
    // Fetch slides after a delay to allow generation
    setTimeout(() => {
      fetchSlides();
    }, 2000);
  };
  
  return (
    <div className="flex h-screen bg-dark text-text-primary">
      <Sidebar projectId={projectId} projectPhase={projectPhase} />
      
      <div className="flex-1 flex flex-col bg-dark-secondary">
        <div className="flex justify-between items-center p-8 border-b border-border">
          <h1 className="text-2xl font-semibold">Presentation Assistant</h1>
          <button
            onClick={createNewProject}
            disabled={loading}
            className="bg-border text-text-primary px-4 py-2 rounded-md hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Creating...' : 'New Project'}
          </button>
        </div>
        
        {error && (
          <div className="mx-8 mt-4 bg-red-900 text-red-200 p-3 rounded-md">
            Error: {error}
          </div>
        )}
        
        <div className="flex-1 flex gap-5 p-8 min-h-0">
          <ChatSection
            projectId={projectId}
            messages={messages}
            setMessages={setMessages}
            loading={loading}
            setLoading={setLoading}
            setError={setError}
            setPresentationPlan={setPresentationPlan}
          />
          
          <PresentationPlan
            plan={presentationPlan}
            projectId={projectId}
            loading={loading}
            setLoading={setLoading}
            setError={setError}
            setProjectPhase={setProjectPhase}
            onPlanApproved={handlePlanApproved}
          />
          
          <SlidesSection slides={slides} />
        </div>
      </div>
    </div>
  );
};

export default App;