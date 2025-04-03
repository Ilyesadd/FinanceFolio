#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module de génération de rapports de dépenses

Ce module permet de générer des rapports PDF détaillés des dépenses.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch, cm

class ExpenseReporter:
    """
    Classe pour générer des rapports de dépenses.
    """
    
    def __init__(self, expense_analyzer):
        """
        Initialise le générateur de rapports avec un analyseur de dépenses.
        
        Args:
            expense_analyzer (ExpenseAnalyzer): Instance de l'analyseur de dépenses
        """
        self.expense_analyzer = expense_analyzer
    
    def generate_pdf_report(self, output_dir):
        """
        Génère un rapport PDF détaillé des dépenses.
        
        Args:
            output_dir (str): Répertoire de sortie pour le rapport PDF
        
        Returns:
            str: Chemin du fichier PDF généré, ou None en cas d'échec
        """
        # Récupérer les dépenses
        expenses = self.expense_analyzer.expense_manager.get_all_expenses()
        
        if expenses.empty:
            return None
        
        # Créer le répertoire de sortie s'il n'existe pas
        os.makedirs(output_dir, exist_ok=True)
        
        # Générer les graphiques pour le rapport
        graphs_dir = os.path.join(output_dir, 'temp_graphs')
        os.makedirs(graphs_dir, exist_ok=True)
        graph_files = self.expense_analyzer.generate_graphs(graphs_dir)
        
        # Définir le nom du fichier de rapport
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"rapport_depenses_{now}.pdf"
        report_path = os.path.join(output_dir, report_filename)
        
        # Créer le document PDF
        doc = SimpleDocTemplate(
            report_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Contenu du document
        story = []
        styles = getSampleStyleSheet()
        
        # Ajouter des styles personnalisés
        styles.add(ParagraphStyle(
            name='Title',
            parent=styles['Heading1'],
            fontSize=18,
            alignment=1,  # Centre
            spaceAfter=12
        ))
        
        styles.add(ParagraphStyle(
            name='Heading2',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=10
        ))
        
        styles.add(ParagraphStyle(
            name='Normal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6
        ))
        
        # Titre du rapport
        title = Paragraph("Rapport de Suivi des Dépenses Personnelles", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 0.5 * cm))
        
        # Date du rapport
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        date_paragraph = Paragraph(f"Généré le: {date_str}", styles['Normal'])
        story.append(date_paragraph)
        story.append(Spacer(1, 1 * cm))
        
        # Résumé des statistiques
        story.append(Paragraph("Résumé des Statistiques", styles['Heading2']))
        stats = self.expense_analyzer.get_statistics()
        
        # Tableau des statistiques générales
        stats_data = [
            ["Métrique", "Valeur"],
            ["Total des dépenses", f"{stats['total']:.2f} €"],
            ["Moyenne des dépenses", f"{stats['mean']:.2f} €"],
            ["Médiane des dépenses", f"{stats['median']:.2f} €"],
            ["Dépense minimale", f"{stats['min']:.2f} €"],
            ["Dépense maximale", f"{stats['max']:.2f} €"],
            ["Nombre de dépenses", f"{stats['count']}"]
        ]
        
        stats_table = Table(stats_data, colWidths=[250, 150])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (1, 0), 12),
            ('BACKGROUND', (0, 1), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ]))
        
        story.append(stats_table)
        story.append(Spacer(1, 0.5 * cm))
        
        # Dépenses par catégorie
        story.append(Paragraph("Dépenses par Catégorie", styles['Heading2']))
        
        # Tableau des dépenses par catégorie
        category_data = [["Catégorie", "Montant"]]
        for category, amount in stats['by_category'].items():
            category_data.append([category, f"{amount:.2f} €"])
        
        category_table = Table(category_data, colWidths=[250, 150])
        category_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (1, 0), 12),
            ('BACKGROUND', (0, 1), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ]))
        
        story.append(category_table)
        story.append(Spacer(1, 1 * cm))
        
        # Ajouter les graphiques au rapport
        story.append(Paragraph("Graphiques", styles['Heading2']))
        
        for graph_file in graph_files:
            # Ajouter une description du graphique
            graph_name = os.path.basename(graph_file).replace('.png', '').replace('_', ' ').title()
            story.append(Paragraph(graph_name, styles['Normal']))
            
            # Ajouter le graphique
            img = Image(graph_file, width=6*inch, height=3*inch)
            story.append(img)
            story.append(Spacer(1, 0.5 * cm))
        
        # Générer le PDF
        doc.build(story)
        
        return report_path