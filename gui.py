#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module d'interface graphique pour l'application de Suivi des Dépenses

Ce module fournit une interface graphique utilisateur pour l'application
de suivi des dépenses personnelles.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from expense_manager import ExpenseManager
from expense_analyzer import ExpenseAnalyzer
from expense_reporter import ExpenseReporter

class ExpenseTrackerGUI:
    """
    Classe pour l'interface graphique de l'application de suivi des dépenses.
    """
    
    def __init__(self, root):
        """
        Initialise l'interface graphique.
        
        Args:
            root (tk.Tk): Fenêtre principale de l'application
        """
        self.root = root
        self.root.title("Suivi des Dépenses Personnelles")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        
        # Définir les répertoires
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Initialiser les composants
        self.expense_manager = ExpenseManager(self.data_dir)
        self.expense_analyzer = ExpenseAnalyzer(self.expense_manager)
        self.expense_reporter = ExpenseReporter(self.expense_analyzer)
        
        # Créer l'interface
        self._create_widgets()
        self._create_menu()
        
        # Charger les données initiales
        self._load_expenses()
    
    def _create_widgets(self):
        """
        Crée les widgets de l'interface graphique.
        """
        # Créer un notebook (onglets)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Onglet 1: Gestion des dépenses
        self.expenses_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.expenses_frame, text="Dépenses")
        
        # Onglet 2: Statistiques
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="Statistiques")
        
        # Onglet 3: Graphiques
        self.graphs_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.graphs_frame, text="Graphiques")
        
        # Configuration de l'onglet Dépenses
        self._setup_expenses_tab()
        
        # Configuration de l'onglet Statistiques
        self._setup_stats_tab()
        
        # Configuration de l'onglet Graphiques
        self._setup_graphs_tab()
    
    def _create_menu(self):
        """
        Crée le menu de l'application.
        """
        menubar = tk.Menu(self.root)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Générer un rapport PDF", command=self._generate_report)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        
        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="À propos", command=self._show_about)
        menubar.add_cascade(label="Aide", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def _setup_expenses_tab(self):
        """
        Configure l'onglet de gestion des dépenses.
        """
        # Frame pour le formulaire d'ajout
        form_frame = ttk.LabelFrame(self.expenses_frame, text="Ajouter une dépense")
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Champs du formulaire
        ttk.Label(form_frame, text="Montant (€):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.amount_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.amount_var, width=15).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Catégorie:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.category_var = tk.StringVar()
        categories = ["Alimentation", "Transport", "Logement", "Loisirs", "Santé", "Éducation", "Autre"]
        ttk.Combobox(form_frame, textvariable=self.category_var, values=categories, width=15).grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.description_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.description_var, width=40).grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Bouton d'ajout
        ttk.Button(form_frame, text="Ajouter", command=self._add_expense).grid(row=2, column=3, padx=5, pady=5, sticky=tk.E)
        
        # Frame pour la liste des dépenses
        list_frame = ttk.LabelFrame(self.expenses_frame, text="Liste des dépenses")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tableau des dépenses
        columns = ("Date", "Montant", "Catégorie", "Description")
        self.expenses_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Définir les en-têtes
        for col in columns:
            self.expenses_tree.heading(col, text=col)
            self.expenses_tree.column(col, width=100)
        
        # Ajouter une scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.expenses_tree.yview)
        self.expenses_tree.configure(yscroll=scrollbar.set)
        
        # Placement des widgets
        self.expenses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _setup_stats_tab(self):
        """
        Configure l'onglet des statistiques.
        """
        # Frame pour les statistiques
        stats_container = ttk.Frame(self.stats_frame)
        stats_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Zone de texte pour afficher les statistiques
        self.stats_text = tk.Text(stats_container, wrap=tk.WORD, height=20, width=50)
        self.stats_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Scrollbar pour la zone de texte
        scrollbar = ttk.Scrollbar(stats_container, orient=tk.VERTICAL, command=self.stats_text.yview)
        self.stats_text.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bouton pour rafraîchir les statistiques
        ttk.Button(self.stats_frame, text="Rafraîchir", command=self._update_statistics).pack(pady=10)
    
    def _setup_graphs_tab(self):
        """
        Configure l'onglet des graphiques.
        """
        # Frame pour les contrôles
        controls_frame = ttk.Frame(self.graphs_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Sélecteur de type de graphique
        ttk.Label(controls_frame, text="Type de graphique:").pack(side=tk.LEFT, padx=5)
        self.graph_type_var = tk.StringVar(value="pie")
        ttk.Radiobutton(controls_frame, text="Camembert", variable=self.graph_type_var, value="pie").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(controls_frame, text="Barres", variable=self.graph_type_var, value="bar").pack(side=tk.LEFT, padx=5)
        
        # Bouton pour générer le graphique
        ttk.Button(controls_frame, text="Générer", command=self._update_graph).pack(side=tk.RIGHT, padx=5)
        
        # Frame pour le graphique
        self.graph_container = ttk.Frame(self.graphs_frame)
        self.graph_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Message initial
        self.graph_msg = ttk.Label(self.graph_container, text="Cliquez sur 'Générer' pour afficher un graphique")
        self.graph_msg.pack(expand=True)
    
    def _load_expenses(self):
        """
        Charge les dépenses dans le tableau.
        """
        # Effacer le tableau
        for item in self.expenses_tree.get_children():
            self.expenses_tree.delete(item)
        
        # Récupérer les dépenses
        expenses = self.expense_manager.get_all_expenses()
        
        if not expenses.empty:
            # Ajouter les dépenses au tableau
            for _, row in expenses.iterrows():
                date = row['Date'].strftime("%Y-%m-%d") if hasattr(row['Date'], 'strftime') else row['Date']
                self.expenses_tree.insert("", tk.END, values=(date, f"{row['Montant']:.2f} €", row['Catégorie'], row['Description']))
    
    def _add_expense(self):
        """
        Ajoute une nouvelle dépense.
        """
        try:
            # Récupérer les valeurs
            amount_str = self.amount_var.get().replace(',', '.')
            amount = float(amount_str)
            category = self.category_var.get()
            description = self.description_var.get()
            
            # Vérifier les valeurs
            if amount <= 0:
                messagebox.showerror("Erreur", "Le montant doit être positif.")
                return
            
            if not category.strip():
                messagebox.showerror("Erreur", "La catégorie ne peut pas être vide.")
                return
            
            # Ajouter la dépense
            success = self.expense_manager.add_expense(amount, category, description)
            
            if success:
                # Réinitialiser les champs
                self.amount_var.set("")
                self.description_var.set("")
                
                # Rafraîchir le tableau
                self._load_expenses()
                
                # Mettre à jour les statistiques et graphiques si les onglets sont actifs
                if self.notebook.index(self.notebook.select()) == 1:  # Onglet Statistiques
                    self._update_statistics()
                elif self.notebook.index(self.notebook.select()) == 2:  # Onglet Graphiques
                    self._update_graph()
                
                messagebox.showinfo("Succès", "Dépense ajoutée avec succès!")
            else:
                messagebox.showerror("Erreur", "Impossible d'ajouter la dépense.")
        
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")
    
    def _update_statistics(self):
        """
        Met à jour l'affichage des statistiques.
        """
        # Effacer le contenu actuel
        self.stats_text.delete(1.0, tk.END)
        
        # Récupérer les statistiques
        stats = self.expense_analyzer.get_statistics()
        
        if not stats:
            self.stats_text.insert(tk.END, "Aucune dépense enregistrée pour calculer les statistiques.")
            return
        
        # Afficher les statistiques générales
        self.stats_text.insert(tk.END, "===== STATISTIQUES DES DÉPENSES =====\n\n")
        self.stats_text.insert(tk.END, f"Total des dépenses: {stats['total']:.2f} €\n")
        self.stats_text.insert(tk.END, f"Nombre de dépenses: {stats['count']}\n")
        self.stats_text.insert(tk.END, f"Moyenne des dépenses: {stats['mean']:.2f} €\n")
        self.stats_text.insert(tk.END, f"Médiane des dépenses: {stats['median']:.2f} €\n")
        self.stats_text.insert(tk.END, f"Dépense minimale: {stats['min']:.2f} €\n")
        self.stats_text.insert(tk.END, f"Dépense maximale: {stats['max']:.2f} €\n\n")
        
        # Afficher les dépenses par catégorie
        self.stats_text.insert(tk.END, "Dépenses par catégorie:\n")
        for category, amount in stats['by_category'].items():
            self.stats_text.insert(tk.END, f"  {category}: {amount:.2f} €\n")
    
    def _update_graph(self):
        """
        Met à jour l'affichage du graphique.
        """
        # Effacer le contenu actuel
        for widget in self.graph_container.winfo_children():
            widget.destroy()
        
        # Récupérer les dépenses par catégorie
        expenses = self.expense_manager.get_all_expenses()
        
        if expenses.empty:
            self.graph_msg = ttk.Label(self.graph_container, text="Aucune dépense enregistrée pour générer un graphique.")
            self.graph_msg.pack(expand=True)
            return
        
        # Récupérer les dépenses par catégorie
        by_category = self.expense_manager.get_expenses_by_category()
        
        # Créer la figure
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Type de graphique
        graph_type = self.graph_type_var.get()
        
        if graph_type == "pie":
            # Graphique en camembert
            ax.pie(by_category, labels=by_category.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            ax.set_title('Répartition des Dépenses par Catégorie')
        else:  # bar
            # Graphique à barres
            by_category.plot(kind='bar', ax=ax)
            ax.set_title('Dépenses par Catégorie')
            ax.set_xlabel('Catégorie')
            ax.set_ylabel('Montant (€)')
            ax.tick_params(axis='x', rotation=45)
        
        # Intégrer le graphique dans l'interface
        canvas = FigureCanvasTkAgg(fig, master=self.graph_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def _generate_report(self):
        """
        Génère un rapport PDF des dépenses.
        """
        report_path = self.expense_reporter.generate_pdf_report(self.reports_dir)
        
        if not report_path:
            messagebox.showinfo("Information", "Aucune dépense enregistrée pour générer un rapport.")
            return
        
        # Demander à l'utilisateur s'il veut ouvrir le rapport
        if messagebox.askyesno("Rapport généré", f"Le rapport a été généré avec succès:\n{os.path.basename(report_path)}\n\nVoulez-vous l'ouvrir maintenant?"):
            # Ouvrir le rapport avec l'application par défaut
            if sys.platform == "win32":
                os.startfile(report_path)
            elif sys.platform == "darwin":  # macOS
                os.system(f"open {report_path}")
            else:  # linux
                os.system(f"xdg-open {report_path}")
    
    def _show_about(self):
        """
        Affiche la boîte de dialogue "À propos".
        """
        messagebox.showinfo(
            "À propos", 
            "Suivi des Dépenses Personnelles\n\n"
            "Une application pour suivre et analyser vos dépenses mensuelles.\n\n"
            "Fonctionnalités:\n"
            "- Saisie des dépenses\n"
            "- Statistiques et graphiques\n"
            "- Génération de rapports PDF"
        )


def main():
    """
    Fonction principale pour lancer l'application GUI.
    """
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()