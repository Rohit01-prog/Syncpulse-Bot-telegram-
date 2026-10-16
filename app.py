"""
app.py
SyncPulse AI · Autonomous Group Project Coordinator
Ultra-Premium 'Antigravity' Fullscreen Glassmorphic Workspace.
Designed to international hackathon standards with:
- Fullscreen responsive fluid layout (100vw x 100vh)
- Translucent frosted glassmorphism (rgba(255, 255, 255, 0.025), blur 24px)
- Deep layer floating cards with smooth micro-interaction hover lift
- Neon active indicators (box-shadow glows)
- Space Grotesk & Plus Jakarta Sans typography
- Integrated AI Copilot Dock with clean markdown rendering
- 1-Click Judge Demo Presets (⚡ Demo Blocker & ✨ Demo Resolve)
"""

import os
import sys
import json
from typing import Dict, Any

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Load environment variables safely
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Verify Flask installation
try:
    from flask import Flask, jsonify, request, render_template_string
except ImportError:
    print("❌ Flask is not installed. Run: pip install flask")
    sys.exit(1)

from agent_brain import AgentBrain

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "syncpulse_antigravity_2026")
brain = AgentBrain()

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SyncPulse AI · Autonomous Project Coordinator</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- FontAwesome 6 -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">

    <style>
        :root {
            --bg-canvas: #07090e;
            --bg-sidebar: rgba(11, 15, 24, 0.85);
            --glass-card: rgba(255, 255, 255, 0.025);
            --glass-card-hover: rgba(255, 255, 255, 0.045);
            --glass-border: rgba(255, 255, 255, 0.08);
            --glass-border-hover: rgba(99, 102, 241, 0.4);
            --text-heading: #ffffff;
            --text-body: #cbd5e1;
            --text-muted: #64748b;
            --neon-blue: #38bdf8;
            --neon-indigo: #6366f1;
            --neon-rose: #f43f5e;
            --neon-emerald: #10b981;
            --neon-amber: #f59e0b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.12);
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.25);
        }

        body {
            background-color: var(--bg-canvas);
            color: var(--text-body);
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            display: flex;
            letter-spacing: -0.015em;
        }

        .space-heading {
            font-family: 'Space Grotesk', sans-serif;
            letter-spacing: -0.03em;
        }
        .mono-font {
            font-family: 'JetBrains Mono', monospace;
        }

        /* Fullscreen Layout: Left Sidebar + Right Workspace */
        .app-sidebar {
            width: 270px;
            height: 100vh;
            background: var(--bg-sidebar);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border-right: 1px solid var(--glass-border);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 1.5rem 1.25rem;
            flex-shrink: 0;
            z-index: 20;
        }

        .app-main {
            flex: 1;
            height: 100vh;
            overflow-y: auto;
            position: relative;
            background: radial-gradient(circle at 10% 10%, rgba(121, 40, 202, 0.09) 0%, transparent 40%),
                        radial-gradient(circle at 90% 15%, rgba(0, 223, 216, 0.07) 0%, transparent 35%),
                        radial-gradient(circle at 50% 90%, rgba(244, 63, 94, 0.05) 0%, transparent 45%),
                        var(--bg-canvas);
            padding: 2rem 2.5rem 4rem 2.5rem;
            display: flex;
            flex-direction: column;
            gap: 1.75rem;
        }

        /* Brand Area in Sidebar */
        .brand-box {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
            margin-bottom: 1.5rem;
        }

        .brand-logo-ring {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: conic-gradient(from 180deg at 50% 50%, #ff0080 0deg, #7928ca 90deg, #0070f3 180deg, #00dfd8 270deg, #ff0080 360deg);
            padding: 2.5px;
            box-shadow: 0 0 18px rgba(121, 40, 202, 0.45);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .brand-logo-inner {
            width: 100%;
            height: 100%;
            background: #090d16;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            font-size: 14px;
        }

        .btn-new-task-trigger {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--glass-border);
            color: #fff;
            border-radius: 12px;
            padding: 9px 14px;
            font-size: 13px;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            transition: all 0.25s ease;
            margin-bottom: 1.5rem;
            cursor: pointer;
        }
        .btn-new-task-trigger:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.2);
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.08);
        }

        .nav-section-title {
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-muted);
            margin-bottom: 8px;
            padding-left: 8px;
        }

        .nav-item-btn {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 9px 12px;
            border-radius: 10px;
            color: #94a3b8;
            font-size: 13px;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.2s ease;
            margin-bottom: 4px;
            cursor: pointer;
            border: 1px solid transparent;
        }
        .nav-item-btn:hover {
            color: #fff;
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.08);
        }
        .nav-item-btn.active {
            color: #fff;
            background: rgba(99, 102, 241, 0.15);
            border-color: rgba(99, 102, 241, 0.35);
            box-shadow: 0 0 16px rgba(99, 102, 241, 0.2);
        }

        /* Team Avatar List */
        .team-member-row {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 7px 10px;
            border-radius: 8px;
            font-size: 12.5px;
            transition: all 0.2s ease;
        }
        .team-member-row:hover {
            background: rgba(255, 255, 255, 0.04);
        }
        .avatar-initials {
            width: 26px;
            height: 26px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            font-weight: 700;
            color: #fff;
        }

        /* Top Bar */
        .topbar-wrapper {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1.5rem;
            width: 100%;
        }

        .search-glass-box {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--glass-border);
            border-radius: 14px;
            padding: 8px 16px;
            display: flex;
            align-items: center;
            gap: 12px;
            width: 380px;
            transition: all 0.25s ease;
        }
        .search-glass-box:focus-within {
            border-color: var(--neon-blue);
            box-shadow: 0 0 18px rgba(56, 189, 248, 0.25);
            background: rgba(255, 255, 255, 0.05);
        }
        .search-glass-input {
            background: transparent;
            border: none;
            color: #fff;
            font-size: 13.5px;
            outline: none;
            width: 100%;
        }

        .top-action-cluster {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .glass-pill-btn {
            background: rgba(255, 255, 255, 0.035);
            border: 1px solid var(--glass-border);
            color: #e2e8f0;
            font-size: 12.5px;
            font-weight: 600;
            padding: 7px 15px;
            border-radius: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.25s ease;
        }
        .glass-pill-btn:hover {
            color: #fff;
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.2);
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
        }

        .pill-telegram {
            background: rgba(0, 112, 243, 0.1);
            border-color: rgba(0, 112, 243, 0.35);
            color: #38bdf8;
            box-shadow: 0 0 15px rgba(0, 112, 243, 0.15);
        }
        .pill-telegram:hover {
            color: #fff;
            box-shadow: 0 0 20px rgba(0, 112, 243, 0.4);
        }

        .pill-demo-blocker {
            background: rgba(244, 63, 94, 0.1);
            border-color: rgba(244, 63, 94, 0.4);
            color: #fb7185;
            box-shadow: 0 0 14px rgba(244, 63, 94, 0.2);
        }
        .pill-demo-blocker:hover {
            color: #fff;
            background: rgba(244, 63, 94, 0.25);
            box-shadow: 0 0 22px rgba(244, 63, 94, 0.45);
        }

        .pill-demo-resolve {
            background: rgba(16, 185, 129, 0.1);
            border-color: rgba(16, 185, 129, 0.4);
            color: #34d399;
            box-shadow: 0 0 14px rgba(16, 185, 129, 0.2);
        }
        .pill-demo-resolve:hover {
            color: #fff;
            background: rgba(16, 185, 129, 0.25);
            box-shadow: 0 0 22px rgba(16, 185, 129, 0.45);
        }

        /* Hero Headline Banner */
        .hero-banner-section {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        .hero-title {
            font-size: 32px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 4px;
        }
        .hero-desc {
            font-size: 14px;
            color: var(--text-muted);
        }

        /* 4 KPI Metric Cards */
        .kpi-metrics-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.25rem;
        }

        .kpi-card {
            background: var(--glass-card);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 1.15rem 1.35rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 10px 25px -10px rgba(0, 0, 0, 0.5);
            transition: all 0.3s ease;
        }
        .kpi-card:hover {
            border-color: var(--glass-border-hover);
            transform: translateY(-3px);
            box-shadow: 0 15px 35px -10px rgba(99, 102, 241, 0.2);
        }
        .kpi-label {
            font-size: 11.5px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 4px;
        }
        .kpi-value {
            font-size: 26px;
            font-weight: 700;
            color: #fff;
        }
        .kpi-icon-pill {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }

        /* Workspace Tab Filters */
        .filter-tabs-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .tab-pills-group {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .filter-tab-pill {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--glass-border);
            color: var(--text-muted);
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 12.5px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .filter-tab-pill:hover {
            color: #fff;
            background: rgba(255, 255, 255, 0.07);
        }
        .filter-tab-pill.active {
            background: #4f46e5;
            color: #fff;
            border-color: #6366f1;
            box-shadow: 0 0 16px rgba(99, 102, 241, 0.45);
        }
        .filter-tab-pill.tab-blocked-alert {
            color: #fb7185;
            border-color: rgba(244, 63, 94, 0.4);
            background: rgba(244, 63, 94, 0.1);
        }

        /* Floating Task Cards Grid */
        .antigravity-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 1.5rem;
        }

        .floating-task-card {
            background: var(--glass-card);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 18px;
            padding: 1.35rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 220px;
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.65), 0 0 1px 1px rgba(255, 255, 255, 0.04);
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
        }

        .floating-task-card:hover {
            transform: translateY(-6px) scale(1.01);
            border-color: var(--glass-border-hover);
            box-shadow: 0 28px 55px -12px rgba(0, 0, 0, 0.85), 0 0 22px rgba(99, 102, 241, 0.25);
        }

        /* Blocked Glowing Card State */
        .floating-task-card.is-blocked-card {
            border: 1.5px solid rgba(244, 63, 94, 0.65) !important;
            background: rgba(38, 12, 20, 0.35) !important;
            box-shadow: 0 0 28px rgba(244, 63, 94, 0.28), 0 20px 40px -15px rgba(0, 0, 0, 0.7) !important;
        }

        .card-meta-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
        }

        .task-code-badge {
            font-size: 11.5px;
            font-weight: 600;
            color: #94a3b8;
        }

        /* Glowing Neon Indicators */
        .neon-status-node {
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            padding: 3.5px 10px;
            border-radius: 6px;
            letter-spacing: 0.04em;
        }
        .neon-status-blocked {
            background: rgba(244, 63, 94, 0.16);
            color: #fb7185;
            box-shadow: 0 0 14px rgba(244, 63, 94, 0.6);
            border: 1px solid rgba(244, 63, 94, 0.4);
        }
        .neon-status-inprogress {
            background: rgba(59, 130, 246, 0.16);
            color: #60a5fa;
            box-shadow: 0 0 14px rgba(59, 130, 246, 0.5);
            border: 1px solid rgba(59, 130, 246, 0.4);
        }
        .neon-status-completed {
            background: rgba(16, 185, 129, 0.16);
            color: #34d399;
            box-shadow: 0 0 14px rgba(16, 185, 129, 0.5);
            border: 1px solid rgba(16, 185, 129, 0.4);
        }
        .neon-status-backlog {
            background: rgba(255, 255, 255, 0.05);
            color: #94a3b8;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .card-task-title {
            font-size: 15.5px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 6px;
            line-height: 1.35;
        }

        .card-task-description {
            font-size: 12.5px;
            color: #94a3b8;
            line-height: 1.5;
            margin-bottom: 14px;
        }

        /* Radar Box on Blocked Cards */
        .blocker-radar-banner {
            background: rgba(244, 63, 94, 0.12);
            border: 1px solid rgba(244, 63, 94, 0.35);
            border-radius: 10px;
            padding: 9px 12px;
            font-size: 12px;
            color: #fca5a5;
            margin-bottom: 14px;
        }

        .card-footer-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-top: 12px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            font-size: 12.5px;
        }

        .assignee-badge {
            display: flex;
            align-items: center;
            gap: 8px;
            color: #e2e8f0;
            font-weight: 500;
        }

        /* AI Copilot Pinned Dock (Linear/Raycast Style) */
        .copilot-dock-card {
            background: var(--glass-card);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: 0 20px 50px -15px rgba(0, 0, 0, 0.7);
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
            margin-top: 1rem;
        }

        .copilot-chat-stream {
            display: flex;
            flex-direction: column;
            gap: 12px;
            max-height: 260px;
            overflow-y: auto;
            padding-right: 6px;
        }

        .copilot-bubble {
            padding: 10px 16px;
            border-radius: 14px;
            font-size: 13.5px;
            line-height: 1.5;
        }
        .copilot-bubble.bot {
            background: rgba(255, 255, 255, 0.045);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #e2e8f0;
            align-self: flex-start;
            max-width: 85%;
        }
        .copilot-bubble.user {
            background: #4f46e5;
            color: #fff;
            align-self: flex-end;
            max-width: 85%;
            box-shadow: 0 0 20px rgba(79, 70, 229, 0.4);
        }

        .copilot-input-shell {
            display: flex;
            align-items: center;
            gap: 10px;
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid var(--glass-border);
            border-radius: 14px;
            padding: 8px 14px;
            transition: all 0.2s ease;
        }
        .copilot-input-shell:focus-within {
            border-color: var(--neon-indigo);
            box-shadow: 0 0 16px rgba(99, 102, 241, 0.25);
        }
        .copilot-input-field {
            background: transparent;
            border: none;
            color: #fff;
            font-size: 13.5px;
            outline: none;
            width: 100%;
        }

        /* Modal styling */
        .modal-content {
            background: #0d121f !important;
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: #fff;
            border-radius: 20px;
        }
        .form-control, .form-select {
            background: rgba(255, 255, 255, 0.04) !important;
            border-color: rgba(255, 255, 255, 0.12) !important;
            color: #fff !important;
            font-size: 13px;
        }
        .form-control:focus, .form-select:focus {
            border-color: var(--neon-blue) !important;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.3) !important;
        }
    </style>
</head>
<body>

    <!-- Left Sleek Sidebar -->
    <aside class="app-sidebar">
        <div>
            <!-- Brand Logo & Title -->
            <a href="#" class="brand-box">
                <div class="brand-logo-ring">
                    <div class="brand-logo-inner">
                        <i class="fa-solid fa-sparkles"></i>
                    </div>
                </div>
                <div>
                    <div class="fw-bold text-white fs-6 space-heading">SyncPulse AI</div>
                    <div class="text-secondary" style="font-size: 10.5px;">Autonomous Coordinator</div>
                </div>
            </a>

            <!-- + New Milestone Trigger Button -->
            <button class="btn-new-task-trigger" data-bs-toggle="modal" data-bs-target="#newTaskModal">
                <span class="d-flex align-items-center gap-2">
                    <i class="fa-solid fa-plus text-primary"></i>
                    <span>New Milestone</span>
                </span>
                <span class="mono-font text-secondary" style="font-size: 10px;">[N]</span>
            </button>

            <!-- Navigation Links -->
            <div class="nav-section-title">Navigation</div>
            <div class="nav-item-btn active" onclick="filterByStatus('all', this)">
                <i class="fa-solid fa-layer-group"></i>
                <span>Active Milestones</span>
                <span class="badge bg-secondary bg-opacity-25 ms-auto rounded-pill px-2" style="font-size: 10px;" id="sideAllCount">5</span>
            </div>
            <div class="nav-item-btn text-danger" onclick="filterByStatus('blocked', this)">
                <i class="fa-solid fa-triangle-exclamation"></i>
                <span>Blocker Radar</span>
                <span class="badge bg-danger ms-auto rounded-pill px-2" style="font-size: 10px;" id="sideBlockedCount">1</span>
            </div>
            <a href="https://t.me/syncpulse_solver_bot" target="_blank" class="nav-item-btn text-info">
                <i class="fa-brands fa-telegram"></i>
                <span>Telegram Bot</span>
            </a>

            <!-- Team Avatars -->
            <div class="nav-section-title mt-4">Project Team</div>
            <div class="d-flex flex-column gap-1">
                <div class="team-member-row">
                    <span class="avatar-initials" style="background: #f43f5e;">KB</span>
                    <div>
                        <div class="text-light fw-semibold" style="font-size: 12px;">Kabir</div>
                        <div class="text-secondary" style="font-size: 10px;">Backend · Payment API</div>
                    </div>
                    <span class="badge bg-danger bg-opacity-20 text-danger ms-auto" style="font-size: 9px;">Blocked</span>
                </div>
                <div class="team-member-row">
                    <span class="avatar-initials" style="background: #3b82f6;">MR</span>
                    <div>
                        <div class="text-light fw-semibold" style="font-size: 12px;">Meera</div>
                        <div class="text-secondary" style="font-size: 10px;">Frontend · Webhooks</div>
                    </div>
                    <span class="badge bg-primary bg-opacity-20 text-primary ms-auto" style="font-size: 9px;">Active</span>
                </div>
                <div class="team-member-row">
                    <span class="avatar-initials" style="background: #10b981;">AY</span>
                    <div>
                        <div class="text-light fw-semibold" style="font-size: 12px;">Aanya</div>
                        <div class="text-secondary" style="font-size: 10px;">AI Engineer · Pitch</div>
                    </div>
                    <span class="badge bg-success bg-opacity-20 text-success ms-auto" style="font-size: 9px;">Shipped</span>
                </div>
            </div>
        </div>

        <!-- Sidebar Bottom Footer -->
        <div class="pt-3 border-top border-secondary border-opacity-25 d-flex align-items-center justify-content-between">
            <div>
                <div class="fw-semibold text-white small">Hackathon Kurukshetra</div>
                <div class="text-secondary mono-font" style="font-size: 10px;">DY Patil Pune · Worcflow.ai</div>
            </div>
            <span class="badge bg-success bg-opacity-20 text-success rounded-pill px-2" style="font-size: 9px;">24H LIVE</span>
        </div>
    </aside>

    <!-- Main Expansive Workspace Area (Full Width & Height) -->
    <main class="app-main">
        
        <!-- Top Bar -->
        <header class="topbar-wrapper">
            <!-- Search ⌘K Box -->
            <div class="search-glass-box">
                <i class="fa-solid fa-magnifying-glass text-secondary"></i>
                <input type="text" class="search-glass-input" id="searchInput" placeholder="Search milestones, blockers, or assignees... (⌘K)" onkeyup="renderCards()">
            </div>

            <!-- Top Action Cluster -->
            <div class="top-action-cluster">
                <a href="https://t.me/syncpulse_solver_bot" target="_blank" class="glass-pill-btn pill-telegram">
                    <i class="fa-brands fa-telegram fs-6"></i>
                    <span>@syncpulse_solver_bot</span>
                </a>
                <button class="glass-pill-btn pill-demo-blocker" onclick="simulateDemoBlocker()" title="Simulate Blocker Detection">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                    <span>⚡ Demo Blocker</span>
                </button>
                <button class="glass-pill-btn pill-demo-resolve" onclick="simulateDemoResolve()" title="Simulate Blocker Resolution">
                    <i class="fa-solid fa-circle-check"></i>
                    <span>✨ Demo Resolve</span>
                </button>
                <button class="glass-pill-btn" onclick="fetchTasks()" title="Refresh Dashboard">
                    <i class="fa-solid fa-rotate-right"></i>
                </button>
            </div>
        </header>

        <!-- Hero Headline Banner -->
        <section class="hero-banner-section">
            <div>
                <h1 class="hero-title space-heading">Autonomous Project Workspace</h1>
                <p class="hero-desc">
                    Proactive Telegram Check-ins · Real-time Blocker Radar · Autonomous Dependency Escalation
                </p>
            </div>
            <div class="d-flex align-items-center gap-2">
                <span class="badge bg-primary bg-opacity-20 text-primary-emphasis mono-font px-3 py-1.5" style="border-radius: 8px;">
                    <i class="fa-solid fa-bolt me-1"></i> AUTONOMOUS LOOP ACTIVE
                </span>
            </div>
        </section>

        <!-- 4 KPI Metrics Cards -->
        <section class="kpi-metrics-row">
            <div class="kpi-card">
                <div>
                    <div class="kpi-label">Project Velocity</div>
                    <div class="kpi-value space-heading" id="kpiVelocity">80%</div>
                </div>
                <div class="kpi-icon-pill" style="background: rgba(16, 185, 129, 0.12); color: #34d399;">
                    <i class="fa-solid fa-gauge-high"></i>
                </div>
            </div>

            <div class="kpi-card">
                <div>
                    <div class="kpi-label">Active Sprints</div>
                    <div class="kpi-value space-heading" id="kpiActive">3 Tasks</div>
                </div>
                <div class="kpi-icon-pill" style="background: rgba(59, 130, 246, 0.12); color: #60a5fa;">
                    <i class="fa-solid fa-person-running"></i>
                </div>
            </div>

            <div class="kpi-card">
                <div>
                    <div class="kpi-label">Blocker Radar</div>
                    <div class="kpi-value space-heading text-danger" id="kpiBlocked">1 Active</div>
                </div>
                <div class="kpi-icon-pill" style="background: rgba(244, 63, 94, 0.12); color: #fb7185;">
                    <i class="fa-solid fa-shield-virus"></i>
                </div>
            </div>

            <div class="kpi-card">
                <div>
                    <div class="kpi-label">Telegram Check-ins</div>
                    <div class="kpi-value space-heading" id="kpiCheckins">100%</div>
                </div>
                <div class="kpi-icon-pill" style="background: rgba(121, 40, 202, 0.12); color: #c084fc;">
                    <i class="fa-solid fa-satellite-dish"></i>
                </div>
            </div>
        </section>

        <!-- Filter Tabs -->
        <section class="filter-tabs-bar">
            <div class="tab-pills-group">
                <span class="filter-tab-pill active" onclick="filterByStatus('all', this)">All Milestones (<span id="countAll">5</span>)</span>
                <span class="filter-tab-pill" onclick="filterByStatus('in_progress', this)">⚡ In Progress (<span id="countInProgress">2</span>)</span>
                <span class="filter-tab-pill tab-blocked-alert" onclick="filterByStatus('blocked', this)">🚨 Blocked Radar (<span id="countBlocked">1</span>)</span>
                <span class="filter-tab-pill" onclick="filterByStatus('completed', this)">✓ Shipped (<span id="countShipped">2</span>)</span>
            </div>
            <button class="glass-pill-btn" data-bs-toggle="modal" data-bs-target="#newTaskModal">
                <i class="fa-solid fa-plus text-primary"></i>
                <span>Add Milestone</span>
            </button>
        </section>

        <!-- Antigravity Floating Task Cards Grid -->
        <section class="antigravity-grid" id="cardsGrid">
            <!-- Cards rendered via JS -->
        </section>

        <!-- AI Copilot Pinned Dock -->
        <section class="copilot-dock-card">
            <div class="d-flex align-items-center justify-content-between">
                <div class="d-flex align-items-center gap-2">
                    <i class="fa-solid fa-robot text-primary fs-5"></i>
                    <span class="fw-bold text-white fs-6 space-heading">SyncPulse AI Copilot</span>
                    <span class="badge bg-primary bg-opacity-20 text-primary-emphasis mono-font" style="font-size: 10px;">REASONING ENGINE READY</span>
                </div>
                <div class="d-flex gap-2">
                    <button class="glass-pill-btn py-1 px-3" style="font-size: 11px;" onclick="sendQuickPrompt('Status summary')">
                        📊 Project Summary
                    </button>
                    <button class="glass-pill-btn py-1 px-3" style="font-size: 11px;" onclick="sendQuickPrompt('Who is currently blocked?')">
                        🛑 Analyze Blockers
                    </button>
                    <button class="glass-pill-btn py-1 px-3" style="font-size: 11px;" onclick="sendQuickPrompt('Add task: Deploy to Vercel priority high assigned to Team Lead')">
                        ➕ Quick Add
                    </button>
                </div>
            </div>

            <!-- Messages Stream -->
            <div class="copilot-chat-stream" id="copilotChat">
                <div class="copilot-bubble bot">
                    👋 <strong>SyncPulse Autonomous Copilot online.</strong> Monitoring team milestone velocity, parsing Telegram responses, and orchestrating dependency unblocking in real time.
                </div>
            </div>

            <!-- Input Bar -->
            <form id="copilotForm" onsubmit="submitCopilotQuery(event)" class="copilot-input-shell">
                <i class="fa-solid fa-sparkles text-primary"></i>
                <input type="text" class="copilot-input-field" id="copilotInput" placeholder="Instruct Copilot (e.g. 'Summarize blockers', 'Check in with Kabir', 'Mark TASK-102 completed')..." autocomplete="off" required>
                <button type="submit" class="btn btn-primary btn-sm rounded-pill px-3 py-1">
                    <i class="fa-solid fa-arrow-up"></i>
                </button>
            </form>
        </section>

    </main>

    <!-- Modal: Create Milestone -->
    <div class="modal fade" id="newTaskModal" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header border-secondary border-opacity-25 px-4 pt-4 pb-2">
                    <h6 class="modal-title fw-bold text-white space-heading">
                        <i class="fa-solid fa-plus-circle text-primary me-2"></i>Create Project Milestone
                    </h6>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <form id="newTaskForm" onsubmit="handleNewTaskSubmit(event)">
                    <div class="modal-body px-4 py-3">
                        <div class="mb-3">
                            <label class="form-label small text-secondary">TITLE *</label>
                            <input type="text" class="form-control" id="taskTitle" placeholder="e.g. Connect Payment Webhooks" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label small text-secondary">DESCRIPTION</label>
                            <textarea class="form-control" id="taskDesc" rows="2.5" placeholder="Scope, requirements, and acceptance criteria..."></textarea>
                        </div>
                        <div class="row g-2 mb-3">
                            <div class="col-6">
                                <label class="form-label small text-secondary">PRIORITY</label>
                                <select class="form-select" id="taskPriority">
                                    <option value="low">Low</option>
                                    <option value="medium" selected>Medium</option>
                                    <option value="high">High</option>
                                    <option value="urgent">Urgent</option>
                                </select>
                            </div>
                            <div class="col-6">
                                <label class="form-label small text-secondary">ASSIGNED TO</label>
                                <input type="text" class="form-control" id="taskAssignee" placeholder="e.g. Kabir, Meera, Aanya">
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label small text-secondary">DUE DATE</label>
                            <input type="date" class="form-control" id="taskDueDate">
                        </div>
                    </div>
                    <div class="modal-footer border-secondary border-opacity-25 px-4 pb-4 pt-2">
                        <button type="button" class="btn btn-secondary btn-sm rounded-pill px-3" data-bs-dismiss="modal">Cancel</button>
                        <button type="submit" class="btn btn-primary btn-sm rounded-pill px-4">Create Milestone</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- Bootstrap 5 JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    
    <script>
        let allTasks = [];
        let currentFilter = 'all';

        async function fetchTasks() {
            try {
                const res = await fetch('/api/tasks');
                allTasks = await res.json();
                renderCards();
            } catch (e) {
                console.error("Error loading tasks:", e);
            }
        }

        function filterByStatus(status, pillEl) {
            currentFilter = status;
            if (pillEl) {
                document.querySelectorAll('.filter-tab-pill, .nav-item-btn').forEach(p => p.classList.remove('active'));
                pillEl.classList.add('active');
            }
            renderCards();
        }

        function renderCards() {
            const query = (document.getElementById('searchInput').value || '').toLowerCase().trim();
            const grid = document.getElementById('cardsGrid');
            grid.innerHTML = '';

            let cAll = allTasks.length;
            let cProg = 0, cBlock = 0, cShip = 0;

            allTasks.forEach(t => {
                const status = (t.status || 'todo').toLowerCase();
                const isBlocked = status === 'blocked' || (t.tags && t.tags.includes('blocked'));

                if (isBlocked) cBlock++;
                else if (status === 'completed') cShip++;
                else if (status === 'in_progress') cProg++;
            });

            // Update Counts
            document.getElementById('countAll').innerText = cAll;
            document.getElementById('countInProgress').innerText = cProg;
            document.getElementById('countBlocked').innerText = cBlock;
            document.getElementById('countShipped').innerText = cShip;
            document.getElementById('sideAllCount').innerText = cAll;
            document.getElementById('sideBlockedCount').innerText = cBlock;

            // Update KPIs
            document.getElementById('kpiActive').innerText = `${cProg} Tasks`;
            document.getElementById('kpiBlocked').innerText = `${cBlock} Active`;
            const velocity = cAll > 0 ? Math.round(((cShip + cProg * 0.5) / cAll) * 100) : 100;
            document.getElementById('kpiVelocity').innerText = `${velocity}%`;

            allTasks.forEach(t => {
                const title = (t.title || '').toLowerCase();
                const owner = (t.assigned_to || '').toLowerCase();
                const id = (t.id || '').toLowerCase();

                if (query && !title.includes(query) && !owner.includes(query) && !id.includes(query)) {
                    return;
                }

                const status = (t.status || 'todo').toLowerCase();
                const isBlocked = status === 'blocked' || (t.tags && t.tags.includes('blocked'));

                // Apply active tab filter
                if (currentFilter === 'blocked' && !isBlocked) return;
                if (currentFilter === 'in_progress' && (status !== 'in_progress' || isBlocked)) return;
                if (currentFilter === 'completed' && status !== 'completed') return;

                const cardHtml = buildFloatingCard(t);
                grid.innerHTML += cardHtml;
            });

            if (grid.innerHTML === '') {
                grid.innerHTML = '<div class="text-secondary py-5 text-center col-12">No matching milestones found.</div>';
            }
        }

        function buildFloatingCard(t) {
            const status = (t.status || 'todo').toLowerCase();
            const isBlocked = status === 'blocked' || (t.tags && t.tags.includes('blocked'));
            const initials = (t.assigned_to || 'UN').substring(0, 2).toUpperCase();

            let statusClass = 'neon-status-backlog';
            let statusText = 'Backlog';

            if (isBlocked) {
                statusClass = 'neon-status-blocked';
                statusText = '🚨 Blocked';
            } else if (status === 'completed') {
                statusClass = 'neon-status-completed';
                statusText = '✓ Shipped';
            } else if (status === 'in_progress') {
                statusClass = 'neon-status-inprogress';
                statusText = '⚡ In Progress';
            }

            // Assign avatar color based on name
            let avatarBg = '#6366f1';
            if (t.assigned_to === 'Kabir') avatarBg = '#f43f5e';
            else if (t.assigned_to === 'Meera') avatarBg = '#3b82f6';
            else if (t.assigned_to === 'Aanya') avatarBg = '#10b981';

            return `
                <div class="floating-task-card ${isBlocked ? 'is-blocked-card' : ''}">
                    <div>
                        <div class="card-meta-header">
                            <span class="task-code-badge mono-font">${t.id}</span>
                            <span class="neon-status-node ${statusClass}">${statusText}</span>
                        </div>

                        <div class="card-task-title">${escapeHtml(t.title)}</div>
                        <div class="card-task-description">${escapeHtml(t.description || 'No description provided.')}</div>

                        ${isBlocked ? `
                            <div class="blocker-radar-banner">
                                <div class="fw-bold"><i class="fa-solid fa-triangle-exclamation me-1"></i> Blocker Detected:</div>
                                <div>Waiting for test credentials from Meera.</div>
                                <div class="mono-font mt-1 d-flex align-items-center justify-content-between" style="font-size:10.5px; color:#f87171;">
                                    <span>Auto-nudge sent to @meera_frontend</span>
                                    <button class="btn btn-sm btn-outline-danger py-0 px-2" style="font-size:9.5px; border-radius:4px;" onclick="updateStatus('${t.id}', 'in_progress')">
                                        Resolve
                                    </button>
                                </div>
                            </div>
                        ` : ''}
                    </div>

                    <div class="card-footer-row">
                        <div class="assignee-badge">
                            <span class="avatar-initials" style="background:${avatarBg}; width:22px; height:22px; font-size:10px;">${initials}</span>
                            <span>${escapeHtml(t.assigned_to || 'Unassigned')}</span>
                        </div>

                        <div class="d-flex align-items-center gap-1.5">
                            ${status !== 'completed' ? `
                                <button class="btn btn-outline-success btn-sm py-0.5 px-2" style="font-size:10.5px; border-radius:6px;" onclick="updateStatus('${t.id}', 'completed')" title="Mark Done">
                                    <i class="fa-solid fa-check"></i> Done
                                </button>
                            ` : ''}
                            ${status !== 'in_progress' ? `
                                <button class="btn btn-outline-primary btn-sm py-0.5 px-2" style="font-size:10.5px; border-radius:6px;" onclick="updateStatus('${t.id}', 'in_progress')" title="Mark In Progress">
                                    <i class="fa-solid fa-play"></i> Start
                                </button>
                            ` : ''}
                            <button class="btn btn-outline-danger btn-sm py-0.5 px-1.5" style="font-size:10.5px; border-radius:6px;" onclick="deleteTask('${t.id}')" title="Delete">
                                <i class="fa-solid fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }

        async function updateStatus(taskId, status) {
            try {
                await fetch(`/api/tasks/${taskId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ status: status, tags: status === 'blocked' ? ['blocked'] : [] })
                });
                fetchTasks();
            } catch (e) {
                console.error(e);
            }
        }

        async function deleteTask(taskId) {
            if (!confirm(`Delete milestone ${taskId}?`)) return;
            try {
                await fetch(`/api/tasks/${taskId}`, { method: 'DELETE' });
                fetchTasks();
            } catch (e) {
                console.error(e);
            }
        }

        async function handleNewTaskSubmit(e) {
            e.preventDefault();
            const payload = {
                title: document.getElementById('taskTitle').value,
                description: document.getElementById('taskDesc').value,
                priority: document.getElementById('taskPriority').value,
                assigned_to: document.getElementById('taskAssignee').value || 'Unassigned',
                due_date: document.getElementById('taskDueDate').value
            };
            try {
                const res = await fetch('/api/tasks', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                if (res.ok) {
                    bootstrap.Modal.getInstance(document.getElementById('newTaskModal')).hide();
                    document.getElementById('newTaskForm').reset();
                    fetchTasks();
                }
            } catch (e) {
                console.error(e);
            }
        }

        async function submitCopilotQuery(e) {
            e.preventDefault();
            const input = document.getElementById('copilotInput');
            const query = input.value.trim();
            if (!query) return;

            appendChatBubble('user', query, false);
            input.value = '';

            try {
                const res = await fetch('/api/agent/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });
                const data = await res.json();
                appendChatBubble('bot', data.response || "Task updated.", true);
                if (data.action_taken) {
                    fetchTasks();
                }
            } catch (e) {
                appendChatBubble('bot', "Error communicating with Agent Brain.", false);
            }
        }

        function sendQuickPrompt(cmd) {
            document.getElementById('copilotInput').value = cmd;
            document.getElementById('copilotForm').dispatchEvent(new Event('submit'));
        }

        function appendChatBubble(sender, text, isMarkdown) {
            const chat = document.getElementById('copilotChat');
            const div = document.createElement('div');
            div.className = `copilot-bubble ${sender === 'user' ? 'user' : 'bot'}`;
            
            if (isMarkdown) {
                div.innerHTML = text
                    .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
                    .replace(/\\n/g, '<br>')
                    .replace(/•/g, '&bull;');
            } else {
                div.innerText = text;
            }

            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }

        // Judge Demo Presets
        async function simulateDemoBlocker() {
            const task = allTasks.find(t => t.id === 'TASK-102') || allTasks[0];
            if (task) {
                await fetch(`/api/tasks/${task.id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ status: 'blocked', tags: ['blocked'] })
                });
            }
            appendChatBubble('user', "The API is connected, but I am waiting for test credentials from Meera.", false);
            appendChatBubble('bot', "🛑 **Blocker Detected via Telegram!** Marked TASK-102 as **BLOCKED**.\\n• Dependency: Meera\\n• Reason: Waiting for test credentials\\n🚀 Autonomous escalation dispatched to Meera (@meera_frontend)!", true);
            fetchTasks();
        }

        async function simulateDemoResolve() {
            const task = allTasks.find(t => t.id === 'TASK-102') || allTasks[0];
            if (task) {
                await fetch(`/api/tasks/${task.id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ status: 'completed', tags: ['shipped'] })
                });
            }
            appendChatBubble('user', "Meera shared the credentials! Integration tested and verified.", false);
            appendChatBubble('bot', "🎉 **Milestone Shipped!** Task marked **COMPLETED**. Blocker resolved!", true);
            fetchTasks();
        }

        function escapeHtml(s) {
            return String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
        }

        // Keyboard Shortcut: Press 'N' to open New Milestone Modal
        document.addEventListener('keydown', (e) => {
            if (e.key.toLowerCase() === 'n' && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
                e.preventDefault();
                new bootstrap.Modal(document.getElementById('newTaskModal')).show();
            }
        });

        document.addEventListener('DOMContentLoaded', () => {
            fetchTasks();
        });
    </script>
</body>
</html>
"""

# =============================================================================
# Web Dashboard & REST API Endpoints
# =============================================================================

@app.route("/")
def index():
    """Serves the fullscreen interactive web dashboard."""
    return render_template_string(DASHBOARD_HTML)

@app.route("/api/summary", methods=["GET"])
def api_summary():
    """Returns project metrics and aggregated stats."""
    return jsonify(brain.get_summary())

@app.route("/api/tasks", methods=["GET"])
def api_get_tasks():
    """Returns task list with optional filtering query parameters."""
    status = request.args.get("status")
    priority = request.args.get("priority")
    search = request.args.get("search")
    tasks = brain.get_tasks(status=status, priority=priority, search=search)
    return jsonify(tasks)

@app.route("/api/tasks", methods=["POST"])
def api_create_task():
    """Creates a new task in tasks.json."""
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "Title is required"}), 400

    new_task = brain.add_task(
        title=title,
        description=data.get("description", ""),
        priority=data.get("priority", "medium"),
        assigned_to=data.get("assigned_to", "Unassigned"),
        due_date=data.get("due_date"),
        tags=data.get("tags")
    )
    return jsonify(new_task), 201

@app.route("/api/tasks/<task_id>", methods=["GET"])
def api_get_task(task_id):
    """Retrieves single task details."""
    task = brain.get_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)

@app.route("/api/tasks/<task_id>", methods=["PUT"])
def api_update_task(task_id):
    """Updates fields or status of an existing task."""
    data = request.get_json() or {}
    updated = brain.update_task(task_id, **data)
    if not updated:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(updated)

@app.route("/api/tasks/<task_id>", methods=["DELETE"])
def api_delete_task(task_id):
    """Deletes task from tasks.json."""
    success = brain.delete_task(task_id)
    if not success:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"success": True, "message": f"Task {task_id} deleted."})

@app.route("/api/agent/chat", methods=["POST"])
def api_agent_chat():
    """Processes natural language instructions through Agent Brain."""
    data = request.get_json() or {}
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    result = brain.process_query(query)
    return jsonify(result)

@app.route("/api/health", methods=["GET"])
def api_health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "SyncPulse AI", "version": "3.0.0"})

def main():
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() in ["true", "1", "yes"]

    print("=" * 65)
    print("🌐 SyncPulse AI Antigravity Fullscreen Workspace")
    print("=" * 65)
    print(f"🚀 Running locally on: http://127.0.0.1:{port}")
    print("Press Ctrl+C to stop the web server.")
    print("=" * 65)

    app.run(host="0.0.0.0", port=port, debug=debug)

if __name__ == "__main__":
    main()
