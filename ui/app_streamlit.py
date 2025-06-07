"""
app_streamlit.py – Unified Streamlit UI for Scraping & Cleaning (B5W2)
----------------------------------------------------------------------

Streamlit app for scraping and cleaning Google Play Store reviews of fintech apps.
Supports scraping by bank, exporting as raw or combined CSVs, and cleaning raw files.

Features:
- Scrape reviews per bank with field selection and export mode
- Clean any raw CSV file from /data/raw/ and track rows dropped
- Download all exports and preview core/full field tables

Author: Nabil Mohamed
"""

import os
import pandas as pd
import streamlit as st
from datetime import datetime
from src.scraper.review_scraper import BankReviewScraper
from src.cleaning.review_cleaner import ReviewDataCleaner


class ReviewScraperApp:
    def __init__(self):
        # Bank display → (Play Store ID, Label)
        self.bank_options = {
            "Commercial Bank of Ethiopia (CBE)": (
                "com.combanketh.mobilebanking",
                "CBE",
            ),
            "Bank of Abyssinia (BOA)": ("com.boa.boaMobileBanking", "BOA"),
            "Dashen Bank": ("com.dashen.dashensuperapp", "Dashen"),
        }

        self.all_fields = [
            "review",
            "rating",
            "date",
            "bank",
            "source",
            "reviewId",
            "userName",
            "userImage",
            "appVersion",
            "repliedAt",
            "replyContent",
            "thumbsUpCount",
        ]

        self.metadata_log = []

    def launch(self):
        st.set_page_config(
            page_title="B5W2 Review App", page_icon="🧾", layout="centered"
        )
        st.title("📱 B5W2 Review Scraper & Cleaner")
        st.markdown("Scrape and clean Google Play reviews for Ethiopian fintech apps.")
        self._section_scraping()
        self._section_cleaning()
        self._render_metadata_log()

    # --------------------------------------------------------------------------
    # 🔍 Section: Scrape Reviews
    # --------------------------------------------------------------------------
    def _section_scraping(self):
        st.header("🛠 Scrape Google Play Reviews")

        col1, col2 = st.columns(2)
        selected_banks = col1.multiselect(
            "Select bank(s)",
            list(self.bank_options.keys()),
            default=list(self.bank_options.keys()),
        )
        review_count = col2.slider("Reviews per bank", 100, 1000, 400, step=100)

        export_mode = st.radio(
            "Export mode",
            ["Individual files per bank", "Single combined file"],
            horizontal=True,
        )
        output_dir = st.text_input("Raw output directory", value="data/raw")
        selected_fields = st.multiselect(
            "Fields to export",
            self.all_fields,
            default=["review", "rating", "date", "bank", "source"],
        )

        if st.button("🚀 Start Scraping"):
            all_rows = []
            os.makedirs(output_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            for display_name in selected_banks:
                app_id, bank_label = self.bank_options[display_name]
                scraper = BankReviewScraper(
                    app_id=app_id, bank_label=bank_label, target_count=review_count
                )

                with st.spinner(f"Scraping {review_count} reviews for {bank_label}..."):
                    try:
                        scraper.scrape_reviews()
                        df = pd.DataFrame(scraper.reviews_raw)
                        export_df = df[selected_fields]

                        if export_mode == "Individual files per bank":
                            file_name = f"reviews_{bank_label}_{timestamp}.csv"
                            path = os.path.join(output_dir, file_name)
                            export_df.to_csv(path, index=False, encoding="utf-8-sig")
                            st.success(
                                f"✅ Exported {len(export_df)} reviews → {file_name}"
                            )
                            self._log_export(
                                "raw",
                                bank_label,
                                len(export_df),
                                0,
                                path,
                                export_df,
                                {},
                            )
                        else:
                            all_rows.append(export_df)

                    except Exception as e:
                        st.error(f"❌ Failed to scrape {bank_label}: {e}")

            if export_mode == "Single combined file" and all_rows:
                combined_df = pd.concat(all_rows, ignore_index=True)
                path = os.path.join(output_dir, f"reviews_all_banks_{timestamp}.csv")
                combined_df.to_csv(path, index=False, encoding="utf-8-sig")
                st.success(f"✅ Combined export saved to {path}")
                self._log_export(
                    "raw", "All Banks", len(combined_df), 0, path, combined_df, {}
                )

    # --------------------------------------------------------------------------
    # 🧹 Section: Clean Reviews
    # --------------------------------------------------------------------------
    def _section_cleaning(self):
        st.header("🧹 Clean Existing Review File")
        uploaded_file = st.file_uploader(
            "📂 Select raw review CSV from /data/raw/", type=["csv"]
        )
        output_dir = st.text_input("Cleaned output directory", value="data/cleaned")

        if st.button("✨ Clean Selected File"):
            if uploaded_file is None:
                st.warning("⚠️ Please select a CSV file to clean.")
                return

            try:
                df_raw = pd.read_csv(uploaded_file)
                raw_count = len(df_raw)

                cleaner = ReviewDataCleaner(raw_path=uploaded_file.name, verbose=True)
                cleaner.df = df_raw
                df_clean = cleaner.clean()
                cleaned_count = len(df_clean)
                dropped = raw_count - cleaned_count
                loss_pct = (dropped / raw_count * 100) if raw_count > 0 else 0

                # KPI breakdowns from internal attributes (must be set in `clean()` logic)
                breakdown = getattr(cleaner, "drop_breakdown", {})
                os.makedirs(output_dir, exist_ok=True)

                base_name = os.path.splitext(os.path.basename(uploaded_file.name))[0]
                cleaned_path = os.path.join(output_dir, f"{base_name}_cleaned.csv")
                df_clean.to_csv(cleaned_path, index=False, encoding="utf-8-sig")

                st.success(f"✅ Cleaned data exported to: {cleaned_path}")
                st.info(f"📉 {dropped} rows dropped ({loss_pct:.2f}%)")

                self._log_export(
                    "cleaned",
                    base_name,
                    cleaned_count,
                    dropped,
                    cleaned_path,
                    df_clean,
                    breakdown,
                )

            except Exception as e:
                st.error(f"❌ Cleaning failed: {e}")

    # --------------------------------------------------------------------------
    # 🧾 Export Log + Download + Preview
    # --------------------------------------------------------------------------
    def _log_export(self, export_type, label, count, dropped, path, df, drop_breakdown):
        self.metadata_log.append(
            {
                "Type": export_type,
                "Label": label,
                "Count": count,
                "Dropped": dropped,
                "DropDetails": drop_breakdown,
                "Path": path,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "PreviewDF": df,
            }
        )

    def _render_metadata_log(self):
        st.sidebar.title("🧾 Export Log")
        if not self.metadata_log:
            st.sidebar.info("No exports yet.")
            return

        latest = self.metadata_log[-1]
        st.sidebar.markdown(f"**{latest['Type'].capitalize()}** – {latest['Label']}")
        st.sidebar.markdown(f"📦 Rows exported: {latest['Count']}")
        st.sidebar.markdown(f"🕒 {latest['Timestamp']}")
        st.sidebar.markdown(f"`{latest['Path']}`")

        if latest["Type"] == "cleaned":
            drop_details = latest.get("DropDetails", {})
            if drop_details:
                st.sidebar.markdown("---")
                st.sidebar.markdown("### 🧹 Cleaning Summary")
                for key, val in drop_details.items():
                    st.sidebar.markdown(f"- {val}")
                total = latest["Dropped"]
                percent = (
                    (total / (total + latest["Count"])) * 100
                    if (total + latest["Count"]) > 0
                    else 0
                )
                st.sidebar.markdown(
                    f"✅ Cleaned dataset has {latest['Count']:,} rows (−{percent:.2f}% loss)"
                )

        with open(latest["Path"], "rb") as f:
            st.sidebar.download_button(
                label="⬇️ Download CSV",
                data=f,
                file_name=os.path.basename(latest["Path"]),
                mime="text/csv",
            )

        if st.sidebar.checkbox("🔍 Preview last export"):
            df = latest["PreviewDF"]
            core_only = st.sidebar.checkbox("Show only core 5 fields", value=True)
            cols = (
                ["review", "rating", "date", "bank", "source"]
                if core_only
                else df.columns
            )
            st.subheader("📊 Preview")
            st.dataframe(df[list(cols)].head(10), use_container_width=True)


# ------------------------------------------------------------------
# 🎯 CLI Entry Point (triggered by run_streamlit.py)
# ------------------------------------------------------------------
def launch_app():
    app = ReviewScraperApp()
    app.launch()
