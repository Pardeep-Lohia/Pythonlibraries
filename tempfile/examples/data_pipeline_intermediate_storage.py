#!/usr/bin/env python3
"""
Example: Using tempfile for intermediate storage in data processing pipelines.

This script demonstrates how to use temporary files and directories for
intermediate data storage during multi-stage data processing pipelines.
"""

import tempfile
import os
import json
import csv
import gzip
import shutil
from pathlib import Path
import time


def simulate_data_ingestion(temp_dir):
    """
    Simulate data ingestion stage - create raw data files.
    """
    print("Stage 1: Data Ingestion")

    # Create raw data files
    raw_data_dir = os.path.join(temp_dir, 'raw_data')
    os.makedirs(raw_data_dir)

    # Simulate different data sources
    data_sources = [
        ('users.json', [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
            {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
        ]),
        ('products.csv', [
            ["id", "name", "price"],
            ["1", "Widget A", "19.99"],
            ["2", "Widget B", "29.99"],
            ["3", "Widget C", "39.99"]
        ]),
        ('logs.txt', [
            "2023-01-01 10:00:00 INFO Starting process",
            "2023-01-01 10:01:00 INFO Processing user data",
            "2023-01-01 10:02:00 INFO Processing product data"
        ])
    ]

    for filename, data in data_sources:
        filepath = os.path.join(raw_data_dir, filename)

        if filename.endswith('.json'):
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        elif filename.endswith('.csv'):
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(data)
        else:  # text file
            with open(filepath, 'w') as f:
                f.write('\n'.join(data))

    print(f"Created {len(data_sources)} raw data files in {raw_data_dir}")
    return raw_data_dir


def data_validation_stage(raw_data_dir, temp_dir):
    """
    Stage 2: Data validation and cleaning.
    """
    print("\nStage 2: Data Validation & Cleaning")

    validated_dir = os.path.join(temp_dir, 'validated_data')
    os.makedirs(validated_dir)

    # Process each raw data file
    for filename in os.listdir(raw_data_dir):
        raw_path = os.path.join(raw_data_dir, filename)
        validated_path = os.path.join(validated_dir, f"validated_{filename}")

        if filename.endswith('.json'):
            # Validate JSON structure
            with open(raw_path, 'r') as f:
                data = json.load(f)

            # Add validation metadata
            validated_data = {
                "metadata": {
                    "source": filename,
                    "validated_at": time.time(),
                    "record_count": len(data)
                },
                "data": data
            }

            with open(validated_path, 'w') as f:
                json.dump(validated_data, f, indent=2)

        elif filename.endswith('.csv'):
            # Validate CSV format and clean data
            with open(raw_path, 'r', newline='') as f:
                reader = csv.reader(f)
                rows = list(reader)

            # Basic validation: ensure all rows have same number of columns
            if len(rows) > 1:
                header_len = len(rows[0])
                valid_rows = [row for row in rows if len(row) == header_len]

                with open(validated_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(valid_rows)

        else:  # text files
            # Basic text cleaning
            with open(raw_path, 'r') as f:
                content = f.read()

            # Remove empty lines and strip whitespace
            cleaned_lines = [line.strip() for line in content.split('\n') if line.strip()]

            with open(validated_path, 'w') as f:
                f.write('\n'.join(cleaned_lines))

    print(f"Validated {len(os.listdir(validated_dir))} files")
    return validated_dir


def data_transformation_stage(validated_dir, temp_dir):
    """
    Stage 3: Data transformation and enrichment.
    """
    print("\nStage 3: Data Transformation")

    transformed_dir = os.path.join(temp_dir, 'transformed_data')
    os.makedirs(transformed_dir)

    # Transform each validated file
    for filename in os.listdir(validated_dir):
        validated_path = os.path.join(validated_dir, filename)
        transformed_path = os.path.join(transformed_dir, f"transformed_{filename}")

        if 'users.json' in filename:
            # Transform user data
            with open(validated_path, 'r') as f:
                content = json.load(f)

            users = content['data']
            transformed_users = []

            for user in users:
                # Add derived fields
                transformed_user = {
                    **user,
                    "username": user["name"].lower(),
                    "domain": user["email"].split('@')[1],
                    "is_active": True
                }
                transformed_users.append(transformed_user)

            with open(transformed_path, 'w') as f:
                json.dump(transformed_users, f, indent=2)

        elif 'products.csv' in filename:
            # Transform product data
            with open(validated_path, 'r', newline='') as f:
                reader = csv.DictReader(f)
                products = list(reader)

            transformed_products = []
            for product in products:
                # Add derived fields and convert types
                transformed_product = {
                    **product,
                    "price_usd": float(product["price"]),
                    "category": "electronics" if "Widget" in product["name"] else "other",
                    "in_stock": True
                }
                transformed_products.append(transformed_product)

            with open(transformed_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=transformed_products[0].keys())
                writer.writeheader()
                writer.writerows(transformed_products)

        else:  # logs
            # Transform log data to structured format
            with open(validated_path, 'r') as f:
                lines = f.readlines()

            structured_logs = []
            for line in lines:
                parts = line.strip().split(' ', 3)
                if len(parts) >= 4:
                    structured_logs.append({
                        "timestamp": f"{parts[0]} {parts[1]}",
                        "level": parts[2],
                        "message": parts[3]
                    })

            with open(transformed_path, 'w') as f:
                json.dump(structured_logs, f, indent=2)

    print(f"Transformed {len(os.listdir(transformed_dir))} files")
    return transformed_dir


def data_aggregation_stage(transformed_dir, temp_dir):
    """
    Stage 4: Data aggregation and analysis.
    """
    print("\nStage 4: Data Aggregation")

    aggregated_dir = os.path.join(temp_dir, 'aggregated_data')
    os.makedirs(aggregated_dir)

    # Aggregate data from all transformed files
    summary = {
        "total_users": 0,
        "total_products": 0,
        "total_log_entries": 0,
        "domains": {},
        "categories": {},
        "log_levels": {}
    }

    for filename in os.listdir(transformed_dir):
        transformed_path = os.path.join(transformed_dir, filename)

        if 'users' in filename:
            with open(transformed_path, 'r') as f:
                users = json.load(f)

            summary["total_users"] = len(users)
            for user in users:
                domain = user.get("domain", "unknown")
                summary["domains"][domain] = summary["domains"].get(domain, 0) + 1

        elif 'products' in filename:
            with open(transformed_path, 'r') as f:
                products = json.load(f)

            summary["total_products"] = len(products)
            for product in products:
                category = product.get("category", "unknown")
                summary["categories"][category] = summary["categories"].get(category, 0) + 1

        elif 'logs' in filename:
            with open(transformed_path, 'r') as f:
                logs = json.load(f)

            summary["total_log_entries"] = len(logs)
            for log in logs:
                level = log.get("level", "unknown")
                summary["log_levels"][level] = summary["log_levels"].get(level, 0) + 1

    # Save aggregated results
    summary_path = os.path.join(aggregated_dir, 'pipeline_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"Aggregated data saved to {summary_path}")
    return aggregated_dir


def data_export_stage(aggregated_dir, temp_dir):
    """
    Stage 5: Final data export and compression.
    """
    print("\nStage 5: Data Export")

    export_dir = os.path.join(temp_dir, 'export')
    os.makedirs(export_dir)

    # Export aggregated data in multiple formats
    summary_path = os.path.join(aggregated_dir, 'pipeline_summary.json')

    with open(summary_path, 'r') as f:
        summary = json.load(f)

    # Export as compressed JSON
    compressed_path = os.path.join(export_dir, 'pipeline_results.json.gz')
    with gzip.open(compressed_path, 'wt', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    # Export as CSV for spreadsheet analysis
    csv_path = os.path.join(export_dir, 'summary.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Metric', 'Value'])

        for key, value in summary.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    writer.writerow([f"{key}.{sub_key}", sub_value])
            else:
                writer.writerow([key, value])

    # Create a final report
    report_path = os.path.join(export_dir, 'pipeline_report.txt')
    with open(report_path, 'w') as f:
        f.write("Data Pipeline Processing Report\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Processing completed at: {time.ctime()}\n\n")

        f.write("Summary Statistics:\n")
        f.write(f"- Total Users: {summary.get('total_users', 0)}\n")
        f.write(f"- Total Products: {summary.get('total_products', 0)}\n")
        f.write(f"- Total Log Entries: {summary.get('total_log_entries', 0)}\n\n")

        f.write("Domain Distribution:\n")
        for domain, count in summary.get('domains', {}).items():
            f.write(f"- {domain}: {count}\n")

        f.write("\nCategory Distribution:\n")
        for category, count in summary.get('categories', {}).items():
            f.write(f"- {category}: {count}\n")

        f.write("\nLog Level Distribution:\n")
        for level, count in summary.get('log_levels', {}).items():
            f.write(f"- {level}: {count}\n")

    print(f"Exported {len(os.listdir(export_dir))} final files")
    return export_dir


def run_data_pipeline():
    """
    Run the complete data processing pipeline using temporary directories.
    """
    print("Starting Data Processing Pipeline with Temporary Storage")
    print("=" * 60)

    # Use TemporaryDirectory for the entire pipeline
    with tempfile.TemporaryDirectory(prefix='data_pipeline_') as pipeline_temp_dir:
        print(f"Pipeline workspace: {pipeline_temp_dir}")

        try:
            # Stage 1: Data Ingestion
            raw_data_dir = simulate_data_ingestion(pipeline_temp_dir)

            # Stage 2: Data Validation
            validated_dir = data_validation_stage(raw_data_dir, pipeline_temp_dir)

            # Stage 3: Data Transformation
            transformed_dir = data_transformation_stage(validated_dir, pipeline_temp_dir)

            # Stage 4: Data Aggregation
            aggregated_dir = data_aggregation_stage(transformed_dir, pipeline_temp_dir)

            # Stage 5: Data Export
            export_dir = data_export_stage(aggregated_dir, pipeline_temp_dir)

            # Show final results
            print("\n" + "=" * 60)
            print("Pipeline Results:")
            print(f"Total temporary files created: {sum(len(files) for _, _, files in os.walk(pipeline_temp_dir))}")
            print(f"Total temporary directories created: {sum(len(dirs) for _, dirs, _ in os.walk(pipeline_temp_dir))}")

            # Display final export files
            print("\nFinal Export Files:")
            for filename in sorted(os.listdir(export_dir)):
                filepath = os.path.join(export_dir, filename)
                size = os.path.getsize(filepath)
                print(f"- {filename} ({size} bytes)")

        except Exception as e:
            print(f"Pipeline failed: {e}")
            raise

    print("\nAll temporary files and directories automatically cleaned up!")


def demonstrate_pipeline_error_recovery():
    """
    Demonstrate error recovery in pipelines using temporary files.
    """
    print("\n" + "=" * 60)
    print("Demonstrating Pipeline Error Recovery")

    with tempfile.TemporaryDirectory(prefix='error_recovery_') as temp_dir:
        # Create checkpoint files for recovery
        checkpoint_dir = os.path.join(temp_dir, 'checkpoints')
        os.makedirs(checkpoint_dir)

        stages = ['ingestion', 'validation', 'transformation', 'aggregation']

        # Simulate partial pipeline completion
        for i, stage in enumerate(stages[:2]):  # Only complete first 2 stages
            checkpoint_file = os.path.join(checkpoint_dir, f'{stage}_complete.json')
            with open(checkpoint_file, 'w') as f:
                json.dump({
                    'stage': stage,
                    'completed_at': time.time(),
                    'files_processed': i + 1
                }, f)

        print("Created recovery checkpoints:")
        for filename in os.listdir(checkpoint_dir):
            print(f"- {filename}")

        # Simulate recovery logic
        completed_stages = []
        for filename in sorted(os.listdir(checkpoint_dir)):
            with open(os.path.join(checkpoint_dir, filename), 'r') as f:
                checkpoint = json.load(f)
                completed_stages.append(checkpoint['stage'])

        print(f"Recovery would resume after stages: {completed_stages}")


def main():
    """
    Run all data pipeline examples.
    """
    print("Data Pipeline Intermediate Storage Examples")
    print("=" * 50)

    run_data_pipeline()
    demonstrate_pipeline_error_recovery()

    print("\n" + "=" * 50)
    print("All examples completed successfully!")


if __name__ == "__main__":
    main()
