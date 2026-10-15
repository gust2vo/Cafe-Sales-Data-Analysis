from pathlib import Path
from extract import create_database_engine, load_data
from transform_refactored import standardize_data
from validate import (
    run_validations,
    summarize_validations
)
from clean import (
    prepare_data_for_cleaning,
    clean_item,
    clean_data
)


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Opções: "item", "quantity", "price", "total", "all"
CLEANING_STEP = "item"


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    engine = create_database_engine()

    try:
        print("Extraindo dados do SQL Server...")
        df = load_data(engine)
        print(f"Registros extraídos: {len(df)}")

        print("Transformando os dados...")
        df = standardize_data(df)

        print("Validando os dados...")
        df = run_validations(df)

        validation_report = summarize_validations(df)

        validation_report_path = (
            PROCESSED_DIR / "validation_report.csv"
        )
        validation_report.to_csv(
            validation_report_path,
            index=False,
        )

        validated_path = PROCESSED_DIR / "validated_data.csv"
        df.to_csv(validated_path, index=False)

        print("\nResumo das validações:")
        print(validation_report.to_string(index=False))

        print("\nLimpando os dados...")

        if CLEANING_STEP == "all":
            cleaned_df = clean_data(df)

        else:
            df_test = prepare_data_for_cleaning(df)

            if CLEANING_STEP == "item":
                cleaned_df = clean_item(df_test)

            elif CLEANING_STEP == "quantity":
                cleaned_df = clean_quantity(df_test)

            elif CLEANING_STEP == "price":
                cleaned_df = clean_price_per_unit(df_test)

            elif CLEANING_STEP == "total":
                cleaned_df = recalculate_total_spent(df_test)

            else:
                raise ValueError(
                    f"Etapa de limpeza desconhecida: {CLEANING_STEP}"
                )

        # Salva os dados após a limpeza
        cleaned_path = PROCESSED_DIR / "cleaned_data.csv"
        cleaned_df.to_csv(cleaned_path, index=False)

        print("\nPrévia dos dados após a limpeza:")
        print(cleaned_df.head(10).to_string(index=False))

        print("\nValores ausentes após a limpeza:")
        print(cleaned_df.isna().sum())

        print("\nPipeline concluído.")
        print(f"Dados validados: {validated_path}")
        print(f"Relatório: {validation_report_path}")
        print(f"Dados após a limpeza: {cleaned_path}")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
