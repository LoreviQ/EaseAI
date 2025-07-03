import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatSection from './components/ChatSection';
import PresentationPlan from './components/PresentationPlan';
import SlideViewer from './components/SlideViewer';

const App = () => {
  const [projectId, setProjectId] = useState(null);
  const [projects, setProjects] = useState([]);
  const [messages, setMessages] = useState([]);
  const [presentationPlan, setPresentationPlan] = useState(null);
  const [slides, setSlides] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [projectPhase, setProjectPhase] = useState('preparation');
  
  const API_BASE = 'http://localhost:8000/v1';
  
  // Fetch all projects on component mount
  useEffect(() => {
    fetchProjects();
  }, []);
  
  const fetchProjects = async () => {
    try {
      const response = await fetch(`${API_BASE}/projects/`);
      if (response.ok) {
        const result = await response.json();
        setProjects(result.projects || []);
      }
    } catch (err) {
      console.error('Failed to fetch projects:', err);
    }
  };
  
  const fetchProjectDetails = async (id) => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch project details
      const projectResponse = await fetch(`${API_BASE}/projects/${id}`);
      if (!projectResponse.ok) throw new Error('Failed to fetch project');
      const project = await projectResponse.json();
      setProjectPhase(project.phase);
      
      // Fetch messages
      try {
        const messagesResponse = await fetch(`${API_BASE}/projects/${id}/messages/`);
        if (messagesResponse.ok) {
          const messagesResult = await messagesResponse.json();
          setMessages(messagesResult.messages || []);
        } else {
          setMessages([]);
        }
      } catch {
        setMessages([]);
      }
      
      // Fetch presentation plan
      try {
        const planResponse = await fetch(`${API_BASE}/projects/${id}/plan/`);
        if (planResponse.ok) {
          const plan = await planResponse.json();
          setPresentationPlan(plan);
        } else {
          setPresentationPlan(null);
        }
      } catch {
        setPresentationPlan(null);
      }
      
      // Fetch slides if available
      try {
        const slidesResponse = await fetch(`${API_BASE}/projects/${id}/slides/`);
        if (slidesResponse.ok) {
          const slidesResult = await slidesResponse.json();
          setSlides(slidesResult.slides || []);
        } else {
          setSlides([]);
        }
      } catch {
        setSlides([]);
      }
      
    } catch (err) {
      setError(err.message);
      setMessages([]);
      setPresentationPlan(null);
      setSlides([]);
    } finally {
      setLoading(false);
    }
  };
  
  const selectProject = (id) => {
    setProjectId(id);
    fetchProjectDetails(id);
  };
  
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
      
      // Refresh projects list
      fetchProjects();
      
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
      <Sidebar 
        projectId={projectId} 
        projectPhase={projectPhase} 
        projects={projects}
        onSelectProject={selectProject}
        onCreateProject={createNewProject}
        loading={loading}
      />
      
      <div className="flex-1 flex flex-col bg-dark-secondary">
        <div className="flex justify-between items-center p-8 border-b border-border">
          <h1 className="text-2xl font-semibold">Presentation Assistant</h1>
          {projectId && (
            <div className="text-text-secondary text-sm">
              Current Project: {projects.find(p => p.id === projectId)?.title || 'Unknown'}
            </div>
          )}
        </div>
        
        {error && (
          <div className="mx-8 mt-4 bg-red-900 text-red-200 p-3 rounded-md">
            Error: {error}
          </div>
        )}
        
        <div className="flex-1 flex gap-4 p-4 min-h-0 max-h-full">
          {/* Phase 1: Only chat when no plan/slides */}
          {!presentationPlan && slides.length === 0 && (
            <div className="flex-1 max-h-full">
              <ChatSection
                projectId={projectId}
                messages={messages}
                setMessages={setMessages}
                loading={loading}
                setLoading={setLoading}
                setError={setError}
                setPresentationPlan={setPresentationPlan}
              />
            </div>
          )}
          
          {/* Phase 2: Chat + plan prominently when plan exists but no slides */}
          {presentationPlan && slides.length === 0 && (
            <>
              <div className="flex-1 max-h-full">
                <ChatSection
                  projectId={projectId}
                  messages={messages}
                  setMessages={setMessages}
                  loading={loading}
                  setLoading={setLoading}
                  setError={setError}
                  setPresentationPlan={setPresentationPlan}
                />
              </div>
              
              <div className="w-96 max-h-full">
                <PresentationPlan
                  plan={presentationPlan}
                  projectId={projectId}
                  loading={loading}
                  setLoading={setLoading}
                  setError={setError}
                  setProjectPhase={setProjectPhase}
                  onPlanApproved={handlePlanApproved}
                  minimized={false}
                />
              </div>
            </>
          )}
          
          {/* Phase 3: Chat to side, slides prominent, no plan */}
          {slides.length > 0 && (
            <>
              <div className="w-80 max-h-full">
                <ChatSection
                  projectId={projectId}
                  messages={messages}
                  setMessages={setMessages}
                  loading={loading}
                  setLoading={setLoading}
                  setError={setError}
                  setPresentationPlan={setPresentationPlan}
                />
              </div>
              
              <div className="flex-1 max-h-full">
                <SlideViewer slides={slides} />
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;