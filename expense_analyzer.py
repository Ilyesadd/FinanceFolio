#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module d'analyse des dépenses

Ce module permet d'analyser les dépenses et de générer des statistiques et des graphiques.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class ExpenseAnalyzer:
    """
    Classe pour analyser les dépenses personnelles.
    """
    
    def __init__(self, expense_manager):
        """
        Initialise l'analyseur de dépenses avec un gestionnaire de dépenses.
        
        Args:
            expense_manager (ExpenseManager): Instance du gestionnaire de dépenses
        """
        self.expense_manager = expense_manager
    
    def get_statistics(self):
        """
        Calcule les statistiques des dépenses.
        
        Returns:
            dict: Dictionnaire contenant les statistiques des dépenses
        """
        expenses = self.expense_manager.get_all_expenses()
        
        if expenses.empty:
            return None
        
        # Statistiques générales
        stats = {
            'total': expenses['Montant'].sum(),
            'mean': expenses['Montant'].mean(),
            'median': expenses['Montant'].median(),
            'min': expenses['Montant'].min(),
            'max': expenses['Montant'].max(),
            'count': len(expenses)
        }
        
        # Statistiques par catégorie
        by_category = self.expense_manager.get_expenses_by_category()
        stats['by_category'] = by_category.to_dict()
        
        return stats
    
    def generate_graphs(self, output_dir):
        """
        Génère des graphiques des dépenses.
        
        Args:
            output_dir (str): Répertoire de sortie pour les graphiques
        
        Returns:
            list: Liste des chemins des fichiers graphiques générés
        """
        expenses = self.expense_manager.get_all_expenses()
        
        if expenses.empty:
            return []
        
        # Créer le répertoire de sortie s'il n'existe pas
        os.makedirs(output_dir, exist_ok=True)
        
        # Liste pour stocker les chemins des fichiers graphiques
        graph_files = []
        
        # Configurer le style des graphiques
        sns.set(style="whitegrid")
        plt.rcParams.update({'font.size': 10})
        
        # 1. Graphique en camembert des dépenses par catégorie
        plt.figure(figsize=(10, 6))
        by_category = self.expense_manager.get_expenses_by_category()
        plt.pie(by_category, labels=by_category.index, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title('Répartition des Dépenses par Catégorie')
        
        # Enregistrer le graphique
        pie_chart_path = os.path.join(output_dir, 'depenses_par_categorie_pie.png')
        plt.savefig(pie_chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        graph_files.append(pie_chart_path)
        
        # 2. Graphique à barres des dépenses par catégorie
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x=by_category.index, y=by_category.values)
        plt.title('Dépenses par Catégorie')
        plt.xlabel('Catégorie')
        plt.ylabel('Montant (€)')
        plt.xticks(rotation=45, ha='right')
        
        # Ajouter les valeurs sur les barres
        for i, v in enumerate(by_category.values):
            ax.text(i, v + 0.1, f"{v:.2f} €", ha='center')
        
        # Enregistrer le graphique
        bar_chart_path = os.path.join(output_dir, 'depenses_par_categorie_bar.png')
        plt.savefig(bar_chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        graph_files.append(bar_chart_path)
        
        # 3. Graphique d'évolution des dépenses dans le temps
        plt.figure(figsize=(12, 6))
        by_date = self.expense_manager.get_expenses_by_date()
        plt.plot(by_date.index, by_date.values, marker='o', linestyle='-')
        plt.title('Évolution des Dépenses dans le Temps')
        plt.xlabel('Date')
        plt.ylabel('Montant (€)')
        plt.grid(True)
        plt.xticks(rotation=45)
        
        # Enregistrer le graphique
        time_chart_path = os.path.join(output_dir, 'evolution_depenses.png')
        plt.savefig(time_chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        graph_files.append(time_chart_path)
        
        return graph_files