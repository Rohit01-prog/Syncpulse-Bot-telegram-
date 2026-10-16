-- ====================================================================
-- SyncPulse AI - Supabase Database Schema
-- Track: W-PS-1 AI Group Project Coordinator (Hackathon Kurukshetra)
-- ====================================================================

-- 1. Enable UUID Extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Projects Table
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed', 'at_risk', 'on_hold')),
    health_score INT DEFAULT 100,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Team Members Table (Dynamic & Unlimited)
CREATE TABLE IF NOT EXISTS team_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    telegram_chat_id TEXT,
    telegram_username TEXT,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'busy', 'blocked')),
    availability TEXT DEFAULT 'Available',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Tasks Table (With First-Class Blocker & Escalation Tracking)
CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_code TEXT NOT NULL, -- e.g. TASK-101
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    assigned_to_id UUID REFERENCES team_members(id) ON DELETE SET NULL,
    assigned_to_name TEXT NOT NULL,
    status TEXT DEFAULT 'todo' CHECK (status IN ('todo', 'in_progress', 'blocked', 'completed')),
    priority TEXT DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    due_date DATE,
    is_blocked BOOLEAN DEFAULT FALSE,
    blocker_reason TEXT,
    blocked_by_member_name TEXT,
    last_followed_up_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Activity & AI Conversation Logs Table
CREATE TABLE IF NOT EXISTS activity_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
    actor TEXT NOT NULL, -- 'Agent Brain' or Member Name
    event_type TEXT NOT NULL CHECK (event_type IN ('bot_followup', 'member_reply', 'status_changed', 'blocker_detected', 'escalation_sent', 'task_created')),
    message TEXT NOT NULL,
    ai_interpretation TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Blocker Escalations Table (Room to Grow: Automated Escalations)
CREATE TABLE IF NOT EXISTS blocker_escalations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    blocked_member TEXT NOT NULL,
    blocking_member TEXT NOT NULL,
    blocker_reason TEXT NOT NULL,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'notified', 'resolved')),
    escalated_at TIMESTAMPTZ DEFAULT NOW(),
    resolved_at TIMESTAMPTZ
);

-- 7. Enable Row Level Security (RLS) & Public Read/Write for Hackathon Prototype
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE team_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE blocker_escalations ENABLE ROW LEVEL SECURITY;

-- Allow anon read/write policies for easy hackathon demo setup
DO $$ BEGIN
    CREATE POLICY "Allow public read on projects" ON projects FOR SELECT USING (true);
    CREATE POLICY "Allow public write on projects" ON projects FOR ALL USING (true);
    
    CREATE POLICY "Allow public read on team_members" ON team_members FOR SELECT USING (true);
    CREATE POLICY "Allow public write on team_members" ON team_members FOR ALL USING (true);
    
    CREATE POLICY "Allow public read on tasks" ON tasks FOR SELECT USING (true);
    CREATE POLICY "Allow public write on tasks" ON tasks FOR ALL USING (true);
    
    CREATE POLICY "Allow public read on activity_logs" ON activity_logs FOR SELECT USING (true);
    CREATE POLICY "Allow public write on activity_logs" ON activity_logs FOR ALL USING (true);
    
    CREATE POLICY "Allow public read on blocker_escalations" ON blocker_escalations FOR SELECT USING (true);
    CREATE POLICY "Allow public write on blocker_escalations" ON blocker_escalations FOR ALL USING (true);
EXCEPTION WHEN others THEN NULL;
END $$;

-- 8. Enable Realtime Publications for Live Dashboard Updates
ALTER PUBLICATION supabase_realtime ADD TABLE projects;
ALTER PUBLICATION supabase_realtime ADD TABLE team_members;
ALTER PUBLICATION supabase_realtime ADD TABLE tasks;
ALTER PUBLICATION supabase_realtime ADD TABLE activity_logs;
ALTER PUBLICATION supabase_realtime ADD TABLE blocker_escalations;

-- ====================================================================
-- SEED DATA (Hackathon Kurukshetra Problem Statement Demo Project)
-- ====================================================================

-- Insert Default Project
INSERT INTO projects (id, name, description, status, health_score)
VALUES (
    'a0000000-0000-0000-0000-000000000001',
    'FinTech Platform Capstone',
    'End-to-end college group project integrating payment gateway, frontend dashboard, and presentation slides.',
    'active',
    85
) ON CONFLICT (id) DO NOTHING;

-- Insert Seed Team Members (From Worcflow Problem Statement Story)
INSERT INTO team_members (id, project_id, name, role, telegram_username, status)
VALUES 
    ('b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'Kabir', 'Backend & Payment API', '@kabir_dev', 'active'),
    ('b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000001', 'Meera', 'Frontend & Integration', '@meera_frontend', 'active'),
    ('b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000001', 'Aanya', 'Documentation & Pitch Deck', '@aanya_lead', 'active')
ON CONFLICT (id) DO NOTHING;

-- Insert Seed Tasks matching the exact hackathon demo scenario
INSERT INTO tasks (id, task_code, project_id, title, description, assigned_to_id, assigned_to_name, status, priority, due_date)
VALUES 
    (
        'c0000000-0000-0000-0000-000000000001',
        'TASK-101',
        'a0000000-0000-0000-0000-000000000001',
        'Finalize Presentation Slides & Pitch Deck',
        'Create pitch deck covering architecture, value proposition, and live demo script.',
        'b0000000-0000-0000-0000-000000000003',
        'Aanya',
        'completed',
        'high',
        CURRENT_DATE + INTERVAL '1 day'
    ),
    (
        'c0000000-0000-0000-0000-000000000002',
        'TASK-102',
        'a0000000-0000-0000-0000-000000000001',
        'Connect the Payment API & Webhook Handlers',
        'Integrate sandbox payment gateway API, verify checkout flow, and listen to payment webhook events.',
        'b0000000-0000-0000-0000-000000000001',
        'Kabir',
        'in_progress',
        'urgent',
        CURRENT_DATE
    ),
    (
        'c0000000-0000-0000-0000-000000000003',
        'TASK-103',
        'a0000000-0000-0000-0000-000000000001',
        'Frontend Dashboard & UI Integration',
        'Build user transaction history, connect with backend endpoints, and handle loading/error states.',
        'b0000000-0000-0000-0000-000000000002',
        'Meera',
        'in_progress',
        'high',
        CURRENT_DATE + INTERVAL '2 days'
    ),
    (
        'c0000000-0000-0000-0000-000000000004',
        'TASK-104',
        'a0000000-0000-0000-0000-000000000001',
        'Security & End-to-End Test Suite',
        'Run automated integration tests and verify JWT authentication header enforcement.',
        'b0000000-0000-0000-0000-000000000001',
        'Kabir',
        'todo',
        'medium',
        CURRENT_DATE + INTERVAL '3 days'
    )
ON CONFLICT (id) DO NOTHING;

-- Seed initial Activity Log
INSERT INTO activity_logs (project_id, actor, event_type, message, ai_interpretation)
VALUES (
    'a0000000-0000-0000-0000-000000000001',
    'Agent Brain',
    'bot_followup',
    'SyncPulse AI initialized project tracking. Monitored 4 tasks across 3 team members.',
    'System ready for autonomous check-ins.'
);
