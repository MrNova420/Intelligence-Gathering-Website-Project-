/**
 * Professional Report Viewer Component
 * Industry-leading report display similar to Spokeo and Social Catfish
 */

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  DocumentTextIcon,
  UserIcon,
  MapPinIcon,
  PhoneIcon,
  EnvelopeIcon,
  CalendarDaysIcon,
  BriefcaseIcon,
  AcademicCapIcon,
  HomeIcon,
  CameraIcon,
  ShareIcon,
  PrinterIcon,
  ArrowDownTrayIcon,
  ShieldCheckIcon,
  ExclamationTriangleIcon,
  StarIcon,
  EyeIcon,
  LockClosedIcon
} from '@heroicons/react/24/outline';

interface PersonData {
  name: string;
  age: number;
  birthDate: string;
  currentAddress: string;
  previousAddresses: string[];
  phones: Array<{
    number: string;
    type: 'mobile' | 'landline' | 'voip';
    carrier?: string;
    location?: string;
    confidence: number;
  }>;
  emails: Array<{
    address: string;
    type: 'personal' | 'work' | 'other';
    verified: boolean;
    confidence: number;
  }>;
  relatives: Array<{
    name: string;
    relationship: string;
    age?: number;
    location?: string;
  }>;
  associates: Array<{
    name: string;
    connection: string;
    location?: string;
  }>;
  socialProfiles: Array<{
    platform: string;
    username: string;
    url: string;
    followers?: number;
    verified: boolean;
  }>;
  employment: Array<{
    company: string;
    position: string;
    duration: string;
    location: string;
  }>;
  education: Array<{
    institution: string;
    degree: string;
    year: string;
  }>;
  properties: Array<{
    address: string;
    type: string;
    value: number;
    yearPurchased: number;
  }>;
  criminalRecords?: Array<{
    type: string;
    date: string;
    location: string;
    status: string;
  }>;
  riskAssessment: {
    score: number;
    level: 'low' | 'medium' | 'high';
    factors: string[];
  };
}

interface ReportViewerProps {
  personData: PersonData;
  reportType: 'basic' | 'professional' | 'premium';
  onUpgrade?: () => void;
}

const ReportViewer: React.FC<ReportViewerProps> = ({ 
  personData, 
  reportType, 
  onUpgrade 
}) => {
  const [activeSection, setActiveSection] = useState('overview');
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);

  const isLocked = (section: string) => {
    const lockedSections = {
      basic: ['employment', 'education', 'properties', 'criminal'],
      professional: ['criminal'],
      premium: []
    };
    return lockedSections[reportType]?.includes(section) || false;
  };

  const sections = [
    { id: 'overview', label: 'Overview', icon: EyeIcon },
    { id: 'contact', label: 'Contact Info', icon: PhoneIcon },
    { id: 'addresses', label: 'Addresses', icon: HomeIcon },
    { id: 'relatives', label: 'Relatives', icon: UserIcon },
    { id: 'social', label: 'Social Media', icon: CameraIcon },
    { id: 'employment', label: 'Employment', icon: BriefcaseIcon },
    { id: 'education', label: 'Education', icon: AcademicCapIcon },
    { id: 'properties', label: 'Properties', icon: HomeIcon },
    { id: 'criminal', label: 'Criminal Records', icon: ShieldCheckIcon }
  ];

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'low': return 'text-green-600 bg-green-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'high': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const SectionHeader: React.FC<{ title: string; icon: React.ComponentType<any>; locked?: boolean }> = ({ 
    title, 
    icon: Icon, 
    locked = false 
  }) => (
    <div className="flex items-center justify-between mb-6">
      <div className="flex items-center">
        <div className="bg-blue-100 p-3 rounded-xl mr-4">
          <Icon className="h-6 w-6 text-blue-600" />
        </div>
        <h3 className="text-2xl font-bold text-gray-900">{title}</h3>
      </div>
      {locked && (
        <button
          onClick={() => setShowUpgradeModal(true)}
          className="flex items-center bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-2 rounded-lg font-semibold hover:shadow-lg transition-all"
        >
          <LockClosedIcon className="h-4 w-4 mr-2" />
          Upgrade to View
        </button>
      )}
    </div>
  );

  const LockedSection: React.FC<{ title: string; description: string }> = ({ title, description }) => (
    <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl p-8 text-center border-2 border-dashed border-gray-300">
      <LockClosedIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
      <h4 className="text-xl font-bold text-gray-700 mb-2">{title}</h4>
      <p className="text-gray-600 mb-6">{description}</p>
      <button
        onClick={() => setShowUpgradeModal(true)}
        className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-xl font-semibold hover:shadow-lg transition-all"
      >
        Upgrade to Access
      </button>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Report Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="bg-gradient-to-br from-blue-100 to-purple-100 p-4 rounded-2xl mr-6">
                <DocumentTextIcon className="h-8 w-8 text-blue-600" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">{personData.name}</h1>
                <p className="text-gray-600">
                  Comprehensive Intelligence Report • Generated {new Date().toLocaleDateString()}
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              <div className={`px-4 py-2 rounded-full font-semibold ${getRiskColor(personData.riskAssessment.level)}`}>
                {personData.riskAssessment.level.toUpperCase()} RISK
              </div>
              
              <div className="flex space-x-2">
                <button className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                  <ShareIcon className="h-5 w-5" />
                </button>
                <button className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                  <PrinterIcon className="h-5 w-5" />
                </button>
                <button className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                  <ArrowDownTrayIcon className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar Navigation */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl shadow-lg p-6 sticky top-8">
              <h3 className="font-bold text-gray-900 mb-4">Report Sections</h3>
              <nav className="space-y-2">
                {sections.map((section) => {
                  const Icon = section.icon;
                  const locked = isLocked(section.id);
                  
                  return (
                    <button
                      key={section.id}
                      onClick={() => !locked && setActiveSection(section.id)}
                      className={`w-full flex items-center px-4 py-3 rounded-xl text-left transition-all ${
                        activeSection === section.id
                          ? 'bg-blue-100 text-blue-700 font-semibold'
                          : locked
                          ? 'text-gray-400 cursor-not-allowed'
                          : 'text-gray-600 hover:bg-gray-100'
                      }`}
                    >
                      <Icon className="h-5 w-5 mr-3" />
                      {section.label}
                      {locked && <LockClosedIcon className="h-4 w-4 ml-auto" />}
                    </button>
                  );
                })}
              </nav>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-2xl shadow-lg">
              <AnimatePresence mode="wait">
                <motion.div
                  key={activeSection}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.3 }}
                  className="p-8"
                >
                  {/* Overview Section */}
                  {activeSection === 'overview' && (
                    <div>
                      <SectionHeader title="Overview" icon={EyeIcon} />
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-6">
                          <h4 className="font-bold text-blue-900 mb-3">Personal Information</h4>
                          <div className="space-y-2 text-blue-800">
                            <p><span className="font-medium">Age:</span> {personData.age} years old</p>
                            <p><span className="font-medium">Birth Date:</span> {personData.birthDate}</p>
                            <p><span className="font-medium">Current Location:</span> {personData.currentAddress}</p>
                          </div>
                        </div>
                        
                        <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-6">
                          <h4 className="font-bold text-purple-900 mb-3">Risk Assessment</h4>
                          <div className="space-y-2">
                            <div className="flex items-center justify-between">
                              <span className="text-purple-800 font-medium">Risk Score:</span>
                              <span className="text-2xl font-bold text-purple-900">{personData.riskAssessment.score}/100</span>
                            </div>
                            <div className="w-full bg-purple-200 rounded-full h-3">
                              <div 
                                className="bg-purple-600 h-3 rounded-full transition-all duration-1000"
                                style={{ width: `${personData.riskAssessment.score}%` }}
                              ></div>
                            </div>
                          </div>
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div className="text-center p-6 bg-gray-50 rounded-xl">
                          <PhoneIcon className="h-12 w-12 text-blue-600 mx-auto mb-3" />
                          <div className="text-2xl font-bold text-gray-900">{personData.phones.length}</div>
                          <div className="text-gray-600">Phone Numbers</div>
                        </div>
                        
                        <div className="text-center p-6 bg-gray-50 rounded-xl">
                          <EnvelopeIcon className="h-12 w-12 text-green-600 mx-auto mb-3" />
                          <div className="text-2xl font-bold text-gray-900">{personData.emails.length}</div>
                          <div className="text-gray-600">Email Addresses</div>
                        </div>
                        
                        <div className="text-center p-6 bg-gray-50 rounded-xl">
                          <UserIcon className="h-12 w-12 text-purple-600 mx-auto mb-3" />
                          <div className="text-2xl font-bold text-gray-900">{personData.relatives.length}</div>
                          <div className="text-gray-600">Known Relatives</div>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Contact Information */}
                  {activeSection === 'contact' && (
                    <div>
                      <SectionHeader title="Contact Information" icon={PhoneIcon} />
                      
                      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                        {/* Phone Numbers */}
                        <div>
                          <h4 className="font-bold text-gray-900 mb-4">Phone Numbers</h4>
                          <div className="space-y-4">
                            {personData.phones.map((phone, index) => (
                              <div key={index} className="border border-gray-200 rounded-xl p-4">
                                <div className="flex items-center justify-between mb-2">
                                  <span className="font-semibold text-lg text-gray-900">{phone.number}</span>
                                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium">
                                    {phone.confidence}% confidence
                                  </span>
                                </div>
                                <div className="text-sm space-y-1 text-gray-600">
                                  <p><span className="font-medium">Type:</span> {phone.type}</p>
                                  {phone.carrier && <p><span className="font-medium">Carrier:</span> {phone.carrier}</p>}
                                  {phone.location && <p><span className="font-medium">Location:</span> {phone.location}</p>}
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>

                        {/* Email Addresses */}
                        <div>
                          <h4 className="font-bold text-gray-900 mb-4">Email Addresses</h4>
                          <div className="space-y-4">
                            {personData.emails.map((email, index) => (
                              <div key={index} className="border border-gray-200 rounded-xl p-4">
                                <div className="flex items-center justify-between mb-2">
                                  <span className="font-semibold text-gray-900">{email.address}</span>
                                  <div className="flex items-center space-x-2">
                                    {email.verified && (
                                      <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium">
                                        Verified
                                      </span>
                                    )}
                                    <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium">
                                      {email.confidence}% confidence
                                    </span>
                                  </div>
                                </div>
                                <p className="text-sm text-gray-600">
                                  <span className="font-medium">Type:</span> {email.type}
                                </p>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Employment Section */}
                  {activeSection === 'employment' && (
                    <div>
                      <SectionHeader 
                        title="Employment History" 
                        icon={BriefcaseIcon} 
                        locked={isLocked('employment')} 
                      />
                      
                      {isLocked('employment') ? (
                        <LockedSection
                          title="Employment History Locked"
                          description="Upgrade to Professional or Premium to access detailed employment history, company information, and career timeline."
                        />
                      ) : (
                        <div className="space-y-6">
                          {personData.employment.map((job, index) => (
                            <div key={index} className="border border-gray-200 rounded-xl p-6">
                              <div className="flex items-start justify-between mb-4">
                                <div>
                                  <h4 className="text-xl font-bold text-gray-900">{job.position}</h4>
                                  <p className="text-lg text-blue-600 font-semibold">{job.company}</p>
                                </div>
                                <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm font-medium">
                                  {job.duration}
                                </span>
                              </div>
                              <p className="text-gray-600 flex items-center">
                                <MapPinIcon className="h-4 w-4 mr-2" />
                                {job.location}
                              </p>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}

                  {/* Add more sections here following the same pattern */}

                </motion.div>
              </AnimatePresence>
            </div>
          </div>
        </div>
      </div>

      {/* Upgrade Modal */}
      <AnimatePresence>
        {showUpgradeModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
          >
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              className="bg-white rounded-2xl p-8 max-w-md w-full"
            >
              <div className="text-center">
                <div className="bg-gradient-to-br from-blue-100 to-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                  <LockClosedIcon className="h-8 w-8 text-blue-600" />
                </div>
                
                <h3 className="text-2xl font-bold text-gray-900 mb-4">
                  Upgrade for Full Access
                </h3>
                
                <p className="text-gray-600 mb-6">
                  Get complete access to employment history, education records, property information, and criminal background checks.
                </p>
                
                <div className="flex space-x-3">
                  <button
                    onClick={() => setShowUpgradeModal(false)}
                    className="flex-1 border border-gray-300 text-gray-700 py-3 rounded-lg font-semibold hover:border-gray-400 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={onUpgrade}
                    className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-all"
                  >
                    Upgrade Now
                  </button>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default ReportViewer;