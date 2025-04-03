


import os
import sys
from expense_manager import ExpenseManager
from expense_analyzer import ExpenseAnalyzer
from expense_reporter import ExpenseReporter

def console_mode():
    # Définir le répertoire de données
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Définir le répertoire de rapports
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Initialiser les composants
    expense_manager = ExpenseManager(data_dir)
    expense_analyzer = ExpenseAnalyzer(expense_manager)
    expense_reporter = ExpenseReporter(expense_analyzer)
    
    while True:
        print("\n===== SUIVI DES DÉPENSES PERSONNELLES =====")
        print("1. Ajouter une dépense")
        print("2. Afficher toutes les dépenses")
        print("3. Afficher les statistiques")
        print("4. Générer des graphiques")
        print("5. Générer un rapport PDF")
        print("0. Quitter")
        
        choice = input("\nVotre choix: ")
        
        if choice == "1":
            add_expense(expense_manager)
        elif choice == "2":
            display_expenses(expense_manager)
        elif choice == "3":
            display_statistics(expense_analyzer)
        elif choice == "4":
            generate_graphs(expense_analyzer, reports_dir)
        elif choice == "5":
            generate_report(expense_reporter, reports_dir)
        elif choice == "0":
            print("Au revoir!")
            sys.exit(0)
        else:
            print("Option invalide. Veuillez réessayer.")

def main():
    # Vérifier si l'argument --console est passé
    if len(sys.argv) > 1 and sys.argv[1] == "--console":
        console_mode()
        return
    
    # Par défaut, lancer l'interface graphique
    try:
        from gui import ExpenseTrackerGUI
        import tkinter as tk
        root = tk.Tk()
        app = ExpenseTrackerGUI(root)
        root.mainloop()
    except ImportError as e:
        print(f"Erreur lors du chargement de l'interface graphique: {e}")
        print("Lancement en mode console...")
        console_mode()
    except Exception as e:
        print(f"Erreur lors du lancement de l'interface graphique: {e}")
        print("Lancement en mode console...")
        console_mode()

def add_expense(expense_manager):
    """Ajoute une nouvelle dépense"""
    try:
        amount = float(input("Montant de la dépense (€): "))
        if amount <= 0:
            print("Le montant doit être positif.")
            return
        
        category = input("Catégorie (ex: Alimentation, Transport, Loisirs): ")
        if not category.strip():
            print("La catégorie ne peut pas être vide.")
            return
        
        description = input("Description (optionnelle): ")
        
        expense_manager.add_expense(amount, category, description)
        print("Dépense ajoutée avec succès!")
    except ValueError:
        print("Erreur: Veuillez entrer un montant valide.")

def display_expenses(expense_manager):
    """Affiche toutes les dépenses"""
    expenses = expense_manager.get_all_expenses()
    
    if expenses.empty:
        print("Aucune dépense enregistrée.")
        return
    
    print("\n===== LISTE DES DÉPENSES =====")
    print(expenses.to_string(index=False))
    print(f"\nTotal: {expenses['Montant'].sum():.2f} €")

def display_statistics(expense_analyzer):
    """Affiche les statistiques des dépenses"""
    stats = expense_analyzer.get_statistics()
    
    if not stats:
        print("Aucune dépense enregistrée pour calculer les statistiques.")
        return
    
    print("\n===== STATISTIQUES DES DÉPENSES =====")
    print(f"Total des dépenses: {stats['total']:.2f} €")
    print(f"Moyenne des dépenses: {stats['mean']:.2f} €")
    print(f"Médiane des dépenses: {stats['median']:.2f} €")
    print(f"Dépense minimale: {stats['min']:.2f} €")
    print(f"Dépense maximale: {stats['max']:.2f} €")
    
    print("\nDépenses par catégorie:")
    for category, amount in stats['by_category'].items():
        print(f"  {category}: {amount:.2f} €")

def generate_graphs(expense_analyzer, output_dir):
    """Génère des graphiques des dépenses"""
    graph_files = expense_analyzer.generate_graphs(output_dir)
    
    if not graph_files:
        print("Aucune dépense enregistrée pour générer des graphiques.")
        return
    
    print("\nGraphiques générés avec succès:")
    for graph_file in graph_files:
        print(f"  - {os.path.basename(graph_file)}")
    print(f"\nLes graphiques sont disponibles dans: {output_dir}")

def generate_report(expense_reporter, output_dir):
    """Génère un rapport PDF des dépenses"""
    report_path = expense_reporter.generate_pdf_report(output_dir)
    
    if not report_path:
        print("Aucune dépense enregistrée pour générer un rapport.")
        return
    
    print(f"\nRapport PDF généré avec succès: {os.path.basename(report_path)}")
    print(f"Le rapport est disponible dans: {output_dir}")

if __name__ == "__main__":
    main()