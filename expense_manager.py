#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module de gestion des dépenses

Ce module permet de gérer les dépenses (ajout, stockage, récupération).
"""

import os
import pandas as pd
from datetime import datetime

class ExpenseManager:
    """
    Classe pour gérer les dépenses personnelles.
    """
    
    def __init__(self, data_dir):
        """
        Initialise le gestionnaire de dépenses.
        
        Args:
            data_dir (str): Répertoire de stockage des données
        """
        self.data_dir = data_dir
        self.data_file = os.path.join(data_dir, 'expenses.csv')
        
        # Créer le répertoire de données s'il n'existe pas
        os.makedirs(data_dir, exist_ok=True)
        
        # Créer le fichier de données s'il n'existe pas
        if not os.path.exists(self.data_file):
            # Créer un DataFrame vide avec les colonnes nécessaires
            columns = ['Date', 'Montant', 'Catégorie', 'Description']
            pd.DataFrame(columns=columns).to_csv(self.data_file, index=False)
    
    def add_expense(self, amount, category, description=""):
        """
        Ajoute une nouvelle dépense.
        
        Args:
            amount (float): Montant de la dépense
            category (str): Catégorie de la dépense
            description (str, optional): Description de la dépense
        
        Returns:
            bool: True si l'ajout a réussi, False sinon
        """
        try:
            # Créer un DataFrame pour la nouvelle dépense
            date = datetime.now().strftime("%Y-%m-%d")
            new_expense = pd.DataFrame({
                'Date': [date],
                'Montant': [float(amount)],
                'Catégorie': [category],
                'Description': [description]
            })
            
            # Lire les dépenses existantes
            if os.path.exists(self.data_file) and os.path.getsize(self.data_file) > 0:
                expenses = pd.read_csv(self.data_file)
                # Ajouter la nouvelle dépense
                expenses = pd.concat([expenses, new_expense], ignore_index=True)
            else:
                expenses = new_expense
            
            # Enregistrer les dépenses
            expenses.to_csv(self.data_file, index=False)
            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout de la dépense: {e}")
            return False
    
    def get_all_expenses(self):
        """
        Récupère toutes les dépenses.
        
        Returns:
            pandas.DataFrame: DataFrame contenant toutes les dépenses
        """
        try:
            if os.path.exists(self.data_file) and os.path.getsize(self.data_file) > 0:
                expenses = pd.read_csv(self.data_file)
                # Convertir la colonne 'Date' en datetime
                expenses['Date'] = pd.to_datetime(expenses['Date'])
                return expenses
            else:
                # Retourner un DataFrame vide avec les colonnes nécessaires
                columns = ['Date', 'Montant', 'Catégorie', 'Description']
                return pd.DataFrame(columns=columns)
        except Exception as e:
            print(f"Erreur lors de la récupération des dépenses: {e}")
            # Retourner un DataFrame vide avec les colonnes nécessaires
            columns = ['Date', 'Montant', 'Catégorie', 'Description']
            return pd.DataFrame(columns=columns)
    
    def get_expenses_by_category(self):
        """
        Récupère les dépenses groupées par catégorie.
        
        Returns:
            pandas.Series: Série contenant les montants totaux par catégorie
        """
        expenses = self.get_all_expenses()
        if expenses.empty:
            return pd.Series()
        
        return expenses.groupby('Catégorie')['Montant'].sum()
    
    def get_expenses_by_date(self):
        """
        Récupère les dépenses groupées par date.
        
        Returns:
            pandas.Series: Série contenant les montants totaux par date
        """
        expenses = self.get_all_expenses()
        if expenses.empty:
            return pd.Series()
        
        # Grouper par date et sommer les montants
        return expenses.groupby(expenses['Date'].dt.date)['Montant'].sum()