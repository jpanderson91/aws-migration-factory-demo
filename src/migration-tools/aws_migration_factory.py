"""
AWS Migration Factory Integration Demo
Demonstrates AWS MGN, Cloud Migration Factory, and portfolio analysis tools
Author: John Anderson - AWS ProServe Migration Specialist Demo
"""

import json
import boto3
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
import time

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class AWSMigrationService:
    """
    AWS Migration service demonstrating enterprise migration capabilities:
    - AWS Application Migration Service (MGN) integration
    - Migration Factory workflow automation
    - Portfolio analysis and discovery tooling
    - Migration wave planning and execution
    """
    
    def __init__(self):
        self.mgn_client = boto3.client('mgn')
        self.ec2_client = boto3.client('ec2')
        self.ssm_client = boto3.client('ssm')
        self.s3_client = boto3.client('s3')
        self.cloudformation_client = boto3.client('cloudformation')
        
    def discover_source_servers(self, discovery_scope: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate server discovery for migration planning
        In real implementation, this would integrate with AWS Application Discovery Service
        """
        try:
            # Simulate discovery results based on scope
            subnet_ranges = discovery_scope.get('subnet_ranges', ['10.0.0.0/24'])
            environment = discovery_scope.get('environment', 'production')
            
            # Mock discovered servers - in reality, this would come from Discovery Agent
            discovered_servers = [
                {
                    'server_id': f'srv-{i:03d}',
                    'hostname': f'{environment}-app-{i:02d}',
                    'ip_address': f'10.0.0.{10 + i}',
                    'os_type': 'Windows' if i % 2 == 0 else 'Linux',
                    'cpu_cores': 4 if i <= 5 else 8,
                    'memory_gb': 16 if i <= 5 else 32,
                    'storage_gb': 100 + (i * 50),
                    'applications': self._get_mock_applications(i),
                    'dependencies': self._get_mock_dependencies(i),
                    'migration_complexity': self._assess_complexity(i),
                    'recommended_instance_type': self._recommend_instance_type(i)
                }
                for i in range(1, 11)  # 10 servers for demo
            ]
            
            # Calculate portfolio summary
            portfolio_summary = {
                'total_servers': len(discovered_servers),
                'windows_servers': len([s for s in discovered_servers if s['os_type'] == 'Windows']),
                'linux_servers': len([s for s in discovered_servers if s['os_type'] == 'Linux']),
                'total_cpu_cores': sum(s['cpu_cores'] for s in discovered_servers),
                'total_memory_gb': sum(s['memory_gb'] for s in discovered_servers),
                'total_storage_gb': sum(s['storage_gb'] for s in discovered_servers),
                'estimated_monthly_cost': self._calculate_migration_cost(discovered_servers)
            }
            
            logger.info("Server discovery completed for %d servers", len(discovered_servers))
            
            return {
                'discovery_id': f"disc-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'discovered_servers': discovered_servers,
                'portfolio_summary': portfolio_summary,
                'discovery_completed_at': datetime.now().isoformat(),
                'next_steps': [
                    'Review server dependencies and migration complexity',
                    'Plan migration waves based on dependencies',
                    'Set up AWS MGN replication for source servers'
                ]
            }
            
        except Exception as e:
            logger.error("Discovery error: %s", str(e))
            return {
                'error': 'Discovery failed',
                'details': str(e)
            }
    
    def create_migration_waves(self, servers: List[Dict[str, Any]], wave_strategy: str = 'dependency_based') -> Dict[str, Any]:
        """
        Create migration waves based on application dependencies and complexity
        Demonstrates migration planning and wave orchestration
        """
        try:
            waves = []
            
            if wave_strategy == 'dependency_based':
                # Group servers by dependency layers
                waves = [
                    {
                        'wave_id': 'wave-001',
                        'wave_name': 'Independent Systems',
                        'description': 'Servers with minimal dependencies - lowest risk',
                        'servers': [s for s in servers if s['migration_complexity'] == 'low'],
                        'estimated_duration_days': 7,
                        'prerequisites': ['MGN replication setup', 'Target VPC configuration']
                    },
                    {
                        'wave_id': 'wave-002', 
                        'wave_name': 'Mid-tier Applications',
                        'description': 'Applications with moderate dependencies',
                        'servers': [s for s in servers if s['migration_complexity'] == 'medium'],
                        'estimated_duration_days': 14,
                        'prerequisites': ['Wave 1 completion', 'Database migration', 'Network connectivity']
                    },
                    {
                        'wave_id': 'wave-003',
                        'wave_name': 'Core Business Systems',
                        'description': 'Critical systems with complex dependencies',
                        'servers': [s for s in servers if s['migration_complexity'] == 'high'],
                        'estimated_duration_days': 21,
                        'prerequisites': ['All previous waves', 'Extended testing', 'Rollback procedures']
                    }
                ]
            
            # Calculate wave timelines
            start_date = datetime.now()
            for i, wave in enumerate(waves):
                wave_start = start_date + timedelta(days=i * 7)  # 1 week between wave starts
                wave['planned_start_date'] = wave_start.isoformat()
                wave['planned_end_date'] = (wave_start + timedelta(days=wave['estimated_duration_days'])).isoformat()
                wave['server_count'] = len(wave['servers'])
            
            logger.info("Migration waves created: %d waves for %d servers", len(waves), len(servers))
            
            return {
                'wave_plan_id': f"plan-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'strategy': wave_strategy,
                'waves': waves,
                'total_migration_duration_days': max(wave['estimated_duration_days'] for wave in waves) + (len(waves) - 1) * 7,
                'risk_assessment': self._assess_migration_risks(waves),
                'created_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error("Wave planning error: %s", str(e))
            return {
                'error': 'Wave planning failed',
                'details': str(e)
            }
    
    def setup_mgn_replication(self, source_servers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Set up AWS MGN replication for source servers
        Demonstrates MGN integration and replication management
        """
        try:
            replication_jobs = []
            
            for server in source_servers[:3]:  # Limit to first 3 for demo
                replication_job = {
                    'source_server_id': server['server_id'],
                    'replication_settings': {
                        'replication_server_instance_type': 't3.small',
                        'replication_servers_security_groups_ids': ['sg-1234567890abcdef0'],
                        'subnet_id': 'subnet-1234567890abcdef0',
                        'use_dedicated_replication_server': False,
                        'default_large_staging_disk_type': 'gp3',
                        'ebs_encryption': 'DEFAULT',
                        'ebs_encryption_key_arn': 'arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012'
                    },
                    'launch_template': {
                        'instance_type': server['recommended_instance_type'],
                        'security_groups': ['sg-production-app'],
                        'subnet_id': 'subnet-production-apps',
                        'iam_instance_profile': 'EC2-MGN-Role',
                        'tags': {
                            'Name': f"Migrated-{server['hostname']}",
                            'Environment': 'Production',
                            'MigrationWave': 'Wave-001',
                            'OriginalServer': server['server_id']
                        }
                    },
                    'replication_status': 'INITIATED',
                    'initial_sync_progress': 0,
                    'last_sync_time': datetime.now().isoformat()
                }
                
                replication_jobs.append(replication_job)
            
            logger.info("MGN replication setup initiated for %d servers", len(replication_jobs))
            
            return {
                'replication_batch_id': f"repl-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'replication_jobs': replication_jobs,
                'estimated_initial_sync_hours': 24,
                'monitoring_dashboard': 'https://console.aws.amazon.com/mgn/home#/sourceServers',
                'next_steps': [
                    'Monitor initial replication progress',
                    'Validate replication settings',
                    'Prepare launch templates for test instances'
                ]
            }
            
        except Exception as e:
            logger.error("MGN setup error: %s", str(e))
            return {
                'error': 'MGN replication setup failed',
                'details': str(e)
            }
    
    def execute_migration_wave(self, wave_id: str, execution_mode: str = 'test') -> Dict[str, Any]:
        """
        Execute a migration wave with proper testing and validation
        Demonstrates migration execution and validation processes
        """
        try:
            execution_plan = {
                'wave_id': wave_id,
                'execution_mode': execution_mode,  # 'test' or 'cutover'
                'execution_id': f"exec-{wave_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'started_at': datetime.now().isoformat(),
                'phases': [
                    {
                        'phase': 'pre_migration_validation',
                        'status': 'completed',
                        'duration_minutes': 15,
                        'validations': [
                            'Replication sync status verified',
                            'Target VPC connectivity confirmed',
                            'Security groups validated',
                            'IAM roles and policies checked'
                        ]
                    },
                    {
                        'phase': 'launch_test_instances',
                        'status': 'in_progress' if execution_mode == 'test' else 'pending',
                        'duration_minutes': 30,
                        'actions': [
                            'Launch instances from MGN',
                            'Apply launch templates',
                            'Configure monitoring',
                            'Update DNS records (test)'
                        ]
                    },
                    {
                        'phase': 'application_validation',
                        'status': 'pending',
                        'duration_minutes': 45,
                        'tests': [
                            'Application functionality testing',
                            'Database connectivity verification',
                            'Performance baseline comparison',
                            'Security configuration validation'
                        ]
                    },
                    {
                        'phase': 'cutover_execution' if execution_mode == 'cutover' else 'test_completion',
                        'status': 'pending',
                        'duration_minutes': 60 if execution_mode == 'cutover' else 15,
                        'actions': [
                            'Final replication sync',
                            'Source server shutdown',
                            'DNS cutover',
                            'Monitoring activation'
                        ] if execution_mode == 'cutover' else [
                            'Test results documentation',
                            'Instance cleanup',
                            'Lessons learned capture'
                        ]
                    }
                ]
            }
            
            # Simulate execution progress
            if execution_mode == 'test':
                execution_plan['estimated_completion'] = (datetime.now() + timedelta(hours=2)).isoformat()
                execution_plan['rollback_plan'] = {
                    'available': True,
                    'procedure': 'Terminate test instances, revert DNS changes',
                    'estimated_time_minutes': 15
                }
            else:
                execution_plan['estimated_completion'] = (datetime.now() + timedelta(hours=4)).isoformat()
                execution_plan['rollback_plan'] = {
                    'available': True,
                    'procedure': 'Restart source servers, revert DNS, investigate issues',
                    'estimated_time_minutes': 60
                }
            
            logger.info("Migration wave execution started: %s (%s mode)", wave_id, execution_mode)
            
            return execution_plan
            
        except Exception as e:
            logger.error("Migration execution error: %s", str(e))
            return {
                'error': 'Migration execution failed',
                'details': str(e),
                'rollback_required': True
            }
    
    def generate_migration_report(self, migration_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive migration assessment and progress report
        Demonstrates reporting and analytics capabilities for stakeholders
        """
        try:
            report = {
                'report_id': f"rpt-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'generated_at': datetime.now().isoformat(),
                'portfolio_analysis': {
                    'servers_discovered': migration_data.get('total_servers', 0),
                    'migration_readiness': {
                        'ready': len([s for s in migration_data.get('servers', []) if s.get('migration_complexity') == 'low']),
                        'needs_remediation': len([s for s in migration_data.get('servers', []) if s.get('migration_complexity') == 'medium']),
                        'complex_migration': len([s for s in migration_data.get('servers', []) if s.get('migration_complexity') == 'high'])
                    }
                },
                'cost_analysis': {
                    'current_estimated_monthly_cost': migration_data.get('current_cost', 0),
                    'target_aws_monthly_cost': migration_data.get('target_cost', 0),
                    'estimated_savings_percentage': 25,  # Typical AWS savings
                    'migration_investment_required': migration_data.get('migration_cost', 0),
                    'roi_months': 12
                },
                'risk_assessment': {
                    'overall_risk_level': 'medium',
                    'key_risks': [
                        'Application dependencies require careful sequencing',
                        'Legacy systems may need modernization',
                        'Network connectivity during transition'
                    ],
                    'mitigation_strategies': [
                        'Implement comprehensive testing in each wave',
                        'Establish robust rollback procedures',
                        'Use AWS MGN for minimal downtime migration'
                    ]
                },
                'timeline_projection': {
                    'total_migration_duration_weeks': 12,
                    'waves_planned': 3,
                    'parallel_execution_opportunities': True,
                    'critical_path_dependencies': [
                        'Network setup and VPN establishment',
                        'Core database migration',
                        'DNS and load balancer configuration'
                    ]
                },
                'recommendations': [
                    'Proceed with Wave 1 (low complexity servers) for quick wins',
                    'Invest in application modernization for legacy systems',
                    'Implement comprehensive monitoring and alerting',
                    'Plan for staff training on AWS services',
                    'Establish cloud governance and cost optimization practices'
                ]
            }
            
            logger.info("Migration report generated: %s", report['report_id'])
            
            return report
            
        except Exception as e:
            logger.error("Report generation error: %s", str(e))
            return {
                'error': 'Report generation failed',
                'details': str(e)
            }
    
    def _get_mock_applications(self, server_index: int) -> List[str]:
        """Generate mock application list based on server index"""
        app_sets = [
            ['Web Server', 'Apache', 'PHP'],
            ['Database', 'SQL Server', 'SSRS'],
            ['Application Server', 'IIS', '.NET Framework'],
            ['File Server', 'Windows File Services'],
            ['Domain Controller', 'Active Directory'],
            ['Monitoring', 'SCOM', 'SQL Express'],
            ['Backup Server', 'Veeam', 'PowerShell'],
            ['ERP System', 'SAP', 'Oracle DB'],
            ['CRM Application', 'Salesforce Connect', 'IIS'],
            ['Analytics Platform', 'Tableau Server', 'PostgreSQL']
        ]
        return app_sets[(server_index - 1) % len(app_sets)]
    
    def _get_mock_dependencies(self, server_index: int) -> List[str]:
        """Generate mock dependency list"""
        if server_index <= 2:
            return []  # Independent servers
        elif server_index <= 6:
            return [f'srv-{server_index - 1:03d}']  # Simple chain dependency
        else:
            return [f'srv-{(server_index - 1) % 5 + 1:03d}', f'srv-{(server_index - 2) % 5 + 1:03d}']  # Multiple dependencies
    
    def _assess_complexity(self, server_index: int) -> str:
        """Assess migration complexity based on server characteristics"""
        if server_index <= 3:
            return 'low'
        elif server_index <= 7:
            return 'medium'
        else:
            return 'high'
    
    def _recommend_instance_type(self, server_index: int) -> str:
        """Recommend AWS instance type based on server specs"""
        if server_index <= 5:
            return 't3.large'  # 4 cores, 16GB
        else:
            return 'm5.xlarge'  # 8 cores, 32GB
    
    def _calculate_migration_cost(self, servers: List[Dict[str, Any]]) -> float:
        """Calculate estimated monthly AWS cost"""
        cost_per_core_hour = 0.05  # Simplified calculation
        hours_per_month = 730
        
        total_cores = sum(server['cpu_cores'] for server in servers)
        return round(total_cores * cost_per_core_hour * hours_per_month, 2)
    
    def _assess_migration_risks(self, waves: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess overall migration risks"""
        total_servers = sum(wave['server_count'] for wave in waves)
        high_complexity_servers = sum(
            len([s for s in wave['servers'] if s['migration_complexity'] == 'high'])
            for wave in waves
        )
        
        risk_percentage = (high_complexity_servers / total_servers) * 100 if total_servers > 0 else 0
        
        if risk_percentage < 20:
            risk_level = 'low'
        elif risk_percentage < 50:
            risk_level = 'medium'
        else:
            risk_level = 'high'
        
        return {
            'overall_risk_level': risk_level,
            'high_complexity_percentage': round(risk_percentage, 1),
            'recommended_testing_weeks': 2 if risk_level == 'high' else 1
        }

# Lambda handler for Migration Factory API
def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler for Migration Factory operations
    """
    
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
    
    try:
        migration_service = AWSMigrationService()
        http_method = event.get('httpMethod', '')
        path = event.get('path', '')
        
        if http_method == 'POST' and path == '/discover-servers':
            body = json.loads(event.get('body', '{}'))
            result = migration_service.discover_source_servers(body.get('discovery_scope', {}))
            
        elif http_method == 'POST' and path == '/create-waves':
            body = json.loads(event.get('body', '{}'))
            result = migration_service.create_migration_waves(
                body.get('servers', []),
                body.get('strategy', 'dependency_based')
            )
            
        elif http_method == 'POST' and path == '/setup-replication':
            body = json.loads(event.get('body', '{}'))
            result = migration_service.setup_mgn_replication(body.get('servers', []))
            
        elif http_method == 'POST' and path == '/execute-wave':
            body = json.loads(event.get('body', '{}'))
            result = migration_service.execute_migration_wave(
                body.get('wave_id', ''),
                body.get('execution_mode', 'test')
            )
            
        elif http_method == 'POST' and path == '/generate-report':
            body = json.loads(event.get('body', '{}'))
            result = migration_service.generate_migration_report(body.get('migration_data', {}))
            
        else:
            result = {
                'message': 'AWS Migration Factory Demo API',
                'available_endpoints': [
                    '/discover-servers',
                    '/create-waves',
                    '/setup-replication',
                    '/execute-wave',
                    '/generate-report'
                ],
                'demo_purpose': 'Showcasing AWS MGN and Migration Factory integration'
            }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        logger.error("Migration handler error: %s", str(e))
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Migration service error',
                'message': 'Please contact your AWS ProServe migration team'
            })
        }
