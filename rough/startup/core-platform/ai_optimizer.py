"""
🤖 ServerAI - AI-Powered Server Management
Advanced AI engine that automatically optimizes server performance, 
predicts issues, and scales resources intelligently.
"""

import asyncio
import json
import time
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import pickle
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler
import redis
import aiohttp

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ServerMetrics:
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: float
    request_count: int
    response_time: float
    error_rate: float
    active_connections: int

@dataclass
class PredictionResult:
    metric_name: str
    current_value: float
    predicted_value: float
    confidence: float
    recommendation: str
    alert_level: AlertSeverity

class AIServerOptimizer:
    """
    🧠 Core AI engine for server optimization
    """
    
    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.models = {}
        self.scalers = {}
        self.anomaly_detectors = {}
        self.initialize_models()
        
    def initialize_models(self):
        """
        🚀 Initialize all AI models
        """
        metrics = ['cpu_usage', 'memory_usage', 'disk_usage', 'response_time', 'error_rate']
        
        for metric in metrics:
            # Prediction model
            self.models[metric] = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            
            # Data scaler
            self.scalers[metric] = StandardScaler()
            
            # Anomaly detector
            self.anomaly_detectors[metric] = IsolationForest(
                contamination=0.1,
                random_state=42
            )
        
        logger.info("🤖 AI models initialized successfully")

    async def collect_metrics(self, server_id: str) -> ServerMetrics:
        """
        📊 Collect real-time server metrics
        """
        try:
            # In real implementation, this would collect from actual servers
            # For demo, we'll simulate realistic metrics
            import random
            
            current_time = datetime.now()
            
            # Simulate realistic server metrics with patterns
            hour = current_time.hour
            day_of_week = current_time.weekday()
            
            # Business hours have higher load
            base_load = 0.3
            if 9 <= hour <= 17 and day_of_week < 5:  # Business hours
                base_load = 0.7
            elif 18 <= hour <= 22:  # Evening peak
                base_load = 0.5
            
            metrics = ServerMetrics(
                timestamp=current_time,
                cpu_usage=min(base_load + random.uniform(-0.2, 0.3), 1.0),
                memory_usage=min(base_load + random.uniform(-0.1, 0.2), 1.0),
                disk_usage=0.4 + random.uniform(-0.1, 0.1),
                network_io=base_load * 1000 + random.uniform(-200, 500),
                request_count=int(base_load * 1000 + random.uniform(-200, 300)),
                response_time=50 + (base_load * 100) + random.uniform(-20, 50),
                error_rate=max(0, (base_load - 0.5) * 0.1 + random.uniform(-0.02, 0.05)),
                active_connections=int(base_load * 100 + random.uniform(-20, 30))
            )
            
            # Store metrics in Redis
            await self.store_metrics(server_id, metrics)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to collect metrics: {e}")
            raise

    async def store_metrics(self, server_id: str, metrics: ServerMetrics):
        """
        💾 Store metrics in Redis for historical analysis
        """
        try:
            key = f"metrics:{server_id}:{metrics.timestamp.isoformat()}"
            data = {
                'cpu_usage': metrics.cpu_usage,
                'memory_usage': metrics.memory_usage,
                'disk_usage': metrics.disk_usage,
                'network_io': metrics.network_io,
                'request_count': metrics.request_count,
                'response_time': metrics.response_time,
                'error_rate': metrics.error_rate,
                'active_connections': metrics.active_connections
            }
            
            # Store with 7 days TTL
            await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: self.redis_client.setex(key, 604800, json.dumps(data))
            )
            
        except Exception as e:
            logger.error(f"Failed to store metrics: {e}")

    async def get_historical_data(self, server_id: str, hours: int = 24) -> List[ServerMetrics]:
        """
        📈 Get historical metrics for analysis
        """
        try:
            pattern = f"metrics:{server_id}:*"
            keys = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: self.redis_client.keys(pattern)
            )
            
            metrics_list = []
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            for key in keys:
                try:
                    # Extract timestamp from key
                    timestamp_str = key.split(':')[-1]
                    timestamp = datetime.fromisoformat(timestamp_str)
                    
                    if timestamp >= cutoff_time:
                        data = await asyncio.get_event_loop().run_in_executor(
                            None, 
                            lambda: json.loads(self.redis_client.get(key))
                        )
                        
                        metrics = ServerMetrics(
                            timestamp=timestamp,
                            **data
                        )
                        metrics_list.append(metrics)
                        
                except Exception as e:
                    logger.warning(f"Failed to parse metrics from key {key}: {e}")
                    continue
            
            # Sort by timestamp
            metrics_list.sort(key=lambda x: x.timestamp)
            return metrics_list
            
        except Exception as e:
            logger.error(f"Failed to get historical data: {e}")
            return []

    def prepare_features(self, metrics_list: List[ServerMetrics]) -> np.ndarray:
        """
        🔧 Prepare features for ML models
        """
        if len(metrics_list) < 2:
            return np.array([])
        
        features = []
        for metrics in metrics_list:
            # Time-based features
            hour = metrics.timestamp.hour
            day_of_week = metrics.timestamp.weekday()
            
            feature_row = [
                metrics.cpu_usage,
                metrics.memory_usage,
                metrics.disk_usage,
                metrics.network_io,
                metrics.request_count,
                metrics.response_time,
                metrics.error_rate,
                metrics.active_connections,
                hour,
                day_of_week,
                # Moving averages (simple approximation)
                np.mean([m.cpu_usage for m in metrics_list[-5:]]),
                np.mean([m.response_time for m in metrics_list[-5:]])
            ]
            features.append(feature_row)
        
        return np.array(features)

    async def predict_metrics(self, server_id: str, minutes_ahead: int = 15) -> List[PredictionResult]:
        """
        🔮 Predict future server metrics using AI
        """
        try:
            # Get historical data
            historical_data = await self.get_historical_data(server_id, hours=72)
            
            if len(historical_data) < 10:
                logger.warning("Insufficient historical data for prediction")
                return []
            
            features = self.prepare_features(historical_data)
            if features.size == 0:
                return []
            
            predictions = []
            target_metrics = ['cpu_usage', 'memory_usage', 'response_time', 'error_rate']
            
            for metric_name in target_metrics:
                try:
                    # Get target values
                    metric_index = {
                        'cpu_usage': 0,
                        'memory_usage': 1,
                        'response_time': 5,
                        'error_rate': 6
                    }[metric_name]
                    
                    target_values = features[:, metric_index]
                    
                    # Train model if we have enough data
                    if len(target_values) >= 5:
                        # Use sliding window for training
                        X = features[:-1]  # All except last
                        y = target_values[1:]  # All except first (shifted target)
                        
                        # Scale features
                        X_scaled = self.scalers[metric_name].fit_transform(X)
                        
                        # Train model
                        self.models[metric_name].fit(X_scaled, y)
                        
                        # Make prediction
                        current_features = features[-1:] # Latest features
                        current_scaled = self.scalers[metric_name].transform(current_features)
                        predicted_value = self.models[metric_name].predict(current_scaled)[0]
                        
                        # Calculate confidence (simplified)
                        confidence = min(0.95, len(historical_data) / 100.0)
                        
                        # Current value
                        current_value = target_values[-1]
                        
                        # Generate recommendation
                        recommendation = self.generate_recommendation(
                            metric_name, current_value, predicted_value
                        )
                        
                        # Determine alert level
                        alert_level = self.determine_alert_level(
                            metric_name, current_value, predicted_value
                        )
                        
                        prediction = PredictionResult(
                            metric_name=metric_name,
                            current_value=current_value,
                            predicted_value=predicted_value,
                            confidence=confidence,
                            recommendation=recommendation,
                            alert_level=alert_level
                        )
                        
                        predictions.append(prediction)
                        
                except Exception as e:
                    logger.error(f"Failed to predict {metric_name}: {e}")
                    continue
            
            return predictions
            
        except Exception as e:
            logger.error(f"Failed to predict metrics: {e}")
            return []

    def generate_recommendation(self, metric_name: str, current: float, predicted: float) -> str:
        """
        💡 Generate intelligent recommendations based on predictions
        """
        change = predicted - current
        change_percent = (change / current) * 100 if current > 0 else 0
        
        recommendations = {
            'cpu_usage': {
                'high': "Consider scaling up CPU resources or optimizing application code",
                'increase': "CPU usage trending upward - monitor closely for scaling needs",
                'normal': "CPU usage is stable and within normal range",
                'decrease': "CPU usage decreasing - potential for cost optimization"
            },
            'memory_usage': {
                'high': "Memory usage is high - investigate memory leaks or scale up RAM",
                'increase': "Memory usage increasing - monitor for potential memory issues",
                'normal': "Memory usage is stable and healthy",
                'decrease': "Memory usage decreasing - good application efficiency"
            },
            'response_time': {
                'high': "Response time is high - check database queries and optimize code",
                'increase': "Response time increasing - investigate performance bottlenecks",
                'normal': "Response time is acceptable and stable",
                'decrease': "Response time improving - good performance optimization"
            },
            'error_rate': {
                'high': "High error rate detected - immediate investigation required",
                'increase': "Error rate increasing - check logs for issues",
                'normal': "Error rate is low and stable",
                'decrease': "Error rate decreasing - system stability improving"
            }
        }
        
        # Determine recommendation category
        if metric_name in ['cpu_usage', 'memory_usage']:
            if predicted > 0.8:
                category = 'high'
            elif change_percent > 20:
                category = 'increase'
            elif change_percent < -20:
                category = 'decrease'
            else:
                category = 'normal'
        elif metric_name == 'response_time':
            if predicted > 1000:  # 1 second
                category = 'high'
            elif change_percent > 30:
                category = 'increase'
            elif change_percent < -30:
                category = 'decrease'
            else:
                category = 'normal'
        elif metric_name == 'error_rate':
            if predicted > 0.05:  # 5%
                category = 'high'
            elif change_percent > 50:
                category = 'increase'
            elif change_percent < -50:
                category = 'decrease'
            else:
                category = 'normal'
        else:
            category = 'normal'
        
        return recommendations.get(metric_name, {}).get(category, "Monitor metric trends")

    def determine_alert_level(self, metric_name: str, current: float, predicted: float) -> AlertSeverity:
        """
        🚨 Determine alert severity based on metric values
        """
        if metric_name in ['cpu_usage', 'memory_usage']:
            if predicted > 0.9 or current > 0.9:
                return AlertSeverity.CRITICAL
            elif predicted > 0.8 or current > 0.8:
                return AlertSeverity.HIGH
            elif predicted > 0.7 or current > 0.7:
                return AlertSeverity.MEDIUM
            else:
                return AlertSeverity.LOW
        
        elif metric_name == 'response_time':
            if predicted > 2000 or current > 2000:  # 2 seconds
                return AlertSeverity.CRITICAL
            elif predicted > 1000 or current > 1000:  # 1 second
                return AlertSeverity.HIGH
            elif predicted > 500 or current > 500:  # 500ms
                return AlertSeverity.MEDIUM
            else:
                return AlertSeverity.LOW
        
        elif metric_name == 'error_rate':
            if predicted > 0.1 or current > 0.1:  # 10%
                return AlertSeverity.CRITICAL
            elif predicted > 0.05 or current > 0.05:  # 5%
                return AlertSeverity.HIGH
            elif predicted > 0.02 or current > 0.02:  # 2%
                return AlertSeverity.MEDIUM
            else:
                return AlertSeverity.LOW
        
        return AlertSeverity.LOW

    async def auto_scale_recommendations(self, server_id: str) -> Dict[str, str]:
        """
        📈 Generate auto-scaling recommendations
        """
        try:
            predictions = await self.predict_metrics(server_id)
            recommendations = {}
            
            for prediction in predictions:
                if prediction.alert_level in [AlertSeverity.HIGH, AlertSeverity.CRITICAL]:
                    if prediction.metric_name == 'cpu_usage':
                        if prediction.predicted_value > 0.8:
                            recommendations['cpu'] = "Scale up: Add 2 more CPU cores"
                        else:
                            recommendations['cpu'] = "Scale up: Add 1 more CPU core"
                    
                    elif prediction.metric_name == 'memory_usage':
                        if prediction.predicted_value > 0.8:
                            recommendations['memory'] = "Scale up: Add 4GB RAM"
                        else:
                            recommendations['memory'] = "Scale up: Add 2GB RAM"
                    
                    elif prediction.metric_name == 'response_time':
                        recommendations['instances'] = "Scale out: Add 2 more instances"
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to generate scaling recommendations: {e}")
            return {}

    async def detect_anomalies(self, server_id: str) -> List[Dict]:
        """
        🔍 Detect anomalies in server behavior
        """
        try:
            historical_data = await self.get_historical_data(server_id, hours=24)
            
            if len(historical_data) < 20:
                return []
            
            features = self.prepare_features(historical_data)
            if features.size == 0:
                return []
            
            anomalies = []
            target_metrics = ['cpu_usage', 'memory_usage', 'response_time', 'error_rate']
            
            for metric_name in target_metrics:
                try:
                    metric_index = {
                        'cpu_usage': 0,
                        'memory_usage': 1,
                        'response_time': 5,
                        'error_rate': 6
                    }[metric_name]
                    
                    metric_values = features[:, metric_index].reshape(-1, 1)
                    
                    # Train anomaly detector
                    self.anomaly_detectors[metric_name].fit(metric_values)
                    
                    # Detect anomalies
                    anomaly_scores = self.anomaly_detectors[metric_name].decision_function(metric_values)
                    anomaly_labels = self.anomaly_detectors[metric_name].predict(metric_values)
                    
                    # Find anomalous points
                    for i, (score, label) in enumerate(zip(anomaly_scores, anomaly_labels)):
                        if label == -1:  # Anomaly detected
                            anomalies.append({
                                'metric': metric_name,
                                'timestamp': historical_data[i].timestamp.isoformat(),
                                'value': float(metric_values[i][0]),
                                'anomaly_score': float(score),
                                'severity': 'high' if score < -0.5 else 'medium'
                            })
                
                except Exception as e:
                    logger.error(f"Failed to detect anomalies for {metric_name}: {e}")
                    continue
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Failed to detect anomalies: {e}")
            return []

# 🚀 Main AI monitoring loop
async def main_ai_loop():
    """
    🔄 Main AI loop that continuously monitors and optimizes servers
    """
    optimizer = AIServerOptimizer()
    server_id = "demo-server-001"
    
    logger.info("🤖 Starting ServerAI monitoring loop...")
    
    while True:
        try:
            # Collect current metrics
            current_metrics = await optimizer.collect_metrics(server_id)
            logger.info(f"📊 CPU: {current_metrics.cpu_usage:.1%}, "
                       f"Memory: {current_metrics.memory_usage:.1%}, "
                       f"Response: {current_metrics.response_time:.0f}ms")
            
            # Generate predictions every 5 minutes
            if int(time.time()) % 300 == 0:  # Every 5 minutes
                predictions = await optimizer.predict_metrics(server_id)
                
                for prediction in predictions:
                    logger.info(f"🔮 {prediction.metric_name}: "
                               f"Current {prediction.current_value:.3f} → "
                               f"Predicted {prediction.predicted_value:.3f} "
                               f"({prediction.confidence:.1%} confidence)")
                    
                    if prediction.alert_level in [AlertSeverity.HIGH, AlertSeverity.CRITICAL]:
                        logger.warning(f"⚠️ {prediction.alert_level.value.upper()}: "
                                     f"{prediction.recommendation}")
                
                # Check for auto-scaling needs
                scaling_recs = await optimizer.auto_scale_recommendations(server_id)
                for resource, recommendation in scaling_recs.items():
                    logger.info(f"📈 Auto-scaling: {resource} - {recommendation}")
            
            # Detect anomalies every 10 minutes
            if int(time.time()) % 600 == 0:  # Every 10 minutes
                anomalies = await optimizer.detect_anomalies(server_id)
                for anomaly in anomalies:
                    logger.warning(f"🔍 Anomaly detected: {anomaly['metric']} = "
                                 f"{anomaly['value']:.3f} at {anomaly['timestamp']}")
            
            # Wait before next collection
            await asyncio.sleep(30)  # Collect metrics every 30 seconds
            
        except KeyboardInterrupt:
            logger.info("👋 Stopping AI monitoring loop...")
            break
        except Exception as e:
            logger.error(f"❌ Error in AI loop: {e}")
            await asyncio.sleep(60)  # Wait 1 minute before retrying

if __name__ == "__main__":
    asyncio.run(main_ai_loop())