# app/services/knowledge_service.py
import requests
from bs4 import BeautifulSoup
import json
from typing import List, Dict, Any

class KnowledgeService:
    def __init__(self):
        self.knowledge_base = self._initialize_knowledge_base()
        print("✅ Service Knowledge (version simplifiée) initialisé !")
    
    def _initialize_knowledge_base(self) -> Dict[str, List[str]]:
        """Base de connaissances santé prédéfinie"""
        return {
            "sommeil": [
                "Dormir 7-9 heures par nuit pour une santé optimale",
                "Éviter les écrans 1 heure avant le coucher pour mieux s'endormir",
                "Maintenir une chambre fraîche (18-20°C) et sombre",
                "Une routine régulière aide à réguler l'horloge biologique"
            ],
            "nutrition": [
                "Manger 5 portions de fruits et légumes par jour",
                "Boire 1.5 à 2L d'eau quotidiennement pour une bonne hydratation",
                "Privilégier les céréales complètes aux céréales raffinées",
                "Inclure des protéines maigres dans chaque repas"
            ],
            "exercice": [
                "30 minutes d'activité modérée par jour améliore la santé cardiovasculaire",
                "Marcher est excellent pour la santé et accessible à tous",
                "Les étirements quotidiens améliorent la flexibilité et réduisent les raideurs",
                "Combiner cardio et renforcement musculaire pour des résultats optimaux"
            ],
            "stress": [
                "La respiration profonde 5-5-5 (inspirer 5s, retenir 5s, expirer 5s) réduit le stress",
                "La méditation 10 minutes par jour aide à se recentrer et calmer l'esprit",
                "Une routine relaxante le soir améliore le sommeil et réduit l'anxiété",
                "L'activité physique régulière est un excellent anti-stress naturel"
            ],
            "mental": [
                "Pratiquer la gratitude quotidienne améliore le bien-être mental",
                "Maintenir des connexions sociales est essentiel pour la santé émotionnelle",
                "Prendre des pauses régulières pendant la journée réduit l'épuisement",
                "Trouver un équilibre entre travail et vie personnelle est crucial"
            ]
        }
    
    async def search_health_resources(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """
        Recherche intelligente dans les connaissances santé
        """
        try:
            query_lower = query.lower()
            results = []
            
            # Recherche par catégorie
            for category, tips in self.knowledge_base.items():
                if self._matches_category(query_lower, category):
                    for i, tip in enumerate(tips[:max_results]):
                        results.append({
                            "content": tip,
                            "metadata": {
                                "source": "Base Connaissances Auriance",
                                "category": category,
                                "confidence": 0.9 - (i * 0.1)  # Score décroissant
                            },
                            "score": 0.9 - (i * 0.1)
                        })
            
            # Si pas de résultats par catégorie, recherche dans tout
            if not results:
                for category, tips in self.knowledge_base.items():
                    for tip in tips:
                        if any(keyword in query_lower for keyword in tip.lower().split()[:3]):
                            results.append({
                                "content": tip,
                                "metadata": {"source": "Base Connaissances", "category": category},
                                "score": 0.7
                            })
                            if len(results) >= max_results:
                                break
            
            return results[:max_results]
            
        except Exception as e:
            print(f"❌ Erreur recherche: {e}")
            return []
    
    def _matches_category(self, query: str, category: str) -> bool:
        """Vérifie si la query correspond à une catégorie"""
        category_keywords = {
            "sommeil": ["sommeil", "dormir", "nuit", "fatigue", "réveil", "insomnie"],
            "nutrition": ["manger", "aliment", "nourriture", "régime", "repas", "diète", "calories"],
            "exercice": ["exercice", "sport", "marche", "activité", "musculation", "entraînement"],
            "stress": ["stress", "anxiété", "relaxation", "détente", "nerveux", "angoisse"],
            "mental": ["mental", "émotion", "bien-être", "humeur", "dépression", "psychologie"]
        }
        
        keywords = category_keywords.get(category, [])
        return any(keyword in query for keyword in keywords)
    
    async def scrape_health_resources(self, topic: str) -> List[Dict[str, Any]]:
        """
        Simulation de scrapping de ressources santé
        """
        # En production, on utiliserait BeautifulSoup pour scraper de vrais sites
        simulated_resources = {
            "sommeil": [
                {
                    "title": "Guide du sommeil réparateur",
                    "content": "Les cycles de sommeil et comment les optimiser pour un repos de qualité",
                    "url": "https://example.com/sommeil",
                    "source": "Ressource Simulée",
                    "category": "sommeil"
                }
            ],
            "nutrition": [
                {
                    "title": "Principes de nutrition équilibrée", 
                    "content": "Les bases d'une alimentation saine et variée pour la santé",
                    "url": "https://example.com/nutrition",
                    "source": "Ressource Simulée",
                    "category": "nutrition"
                }
            ]
        }
        
        return simulated_resources.get(topic.lower(), [])