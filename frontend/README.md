# Frontend - Intelligence Gathering Platform

This directory contains the frontend applications for the Intelligence Gathering Platform.

## 📁 Structure

```
frontend/
├── components/            # Next.js React components
├── pages/                # Next.js pages and routing
├── styles/               # CSS and styling files
├── legacy-web/           # Legacy Flask web interface
│   ├── static/          # Static assets (CSS, JS, images)
│   ├── templates/       # HTML templates
│   └── app.py           # Flask application
├── package.json          # Node.js dependencies
├── next.config.js        # Next.js configuration
└── tailwind.config.js    # Tailwind CSS configuration
```

## 🚀 Quick Start

### Next.js Application (Modern)
```bash
cd frontend
npm install
npm run dev
```

### Legacy Web Interface
The legacy Flask-based web interface is located in `legacy-web/` and is served by the main backend application.

## 🛠️ Technologies

### Modern Stack (Next.js)
- **Next.js 14**: React framework with SSR/SSG
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **React Query**: Data fetching and caching
- **Framer Motion**: Animation library
- **Chart.js**: Data visualization

### Legacy Stack (Flask Templates)
- **Jinja2 Templates**: Server-side templating
- **Vanilla JavaScript**: Client-side functionality
- **Custom CSS**: Styling and themes
- **Progressive Web App**: PWA features

## 🎨 UI Components

The modern frontend includes:
- Professional dashboard interfaces
- Interactive charts and analytics
- Responsive design
- Dark/light theme support
- Mobile-first approach

## 🔧 Development

### Next.js Development
```bash
cd frontend
npm run dev          # Development server
npm run build        # Production build
npm run start        # Production server
npm run lint         # ESLint checking
```

### Styling
- Tailwind CSS for utility classes
- Custom CSS for specific components
- Responsive design principles
- Accessibility considerations

## 🌐 Integration

The frontend integrates with the backend API:
- RESTful API communication
- Real-time data updates
- Authentication handling
- Error management