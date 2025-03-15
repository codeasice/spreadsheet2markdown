import streamlit as st
import pandas as pd
import os
import zipfile
from io import BytesIO

st.title("Markdown Generator from Spreadsheet")
st.markdown("Transform your Excel spreadsheets into well-structured markdown files with YAML frontmatter.")

# Configuration sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    output_dir = st.text_input(
        "Output Directory",
        value="generated_markdown",
        help="Directory where markdown files will be generated"
    )
    if not output_dir:
        st.error("Output directory cannot be empty")
        output_dir = "generated_markdown"

# File upload
st.markdown("### 📤 Upload Your Spreadsheet")
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # File and folder selection
    st.markdown("### 📁 File Organization")
    col1, col2 = st.columns(2)
    with col1:
        filename_col = st.selectbox(
            "Select column for filename",
            df.columns,
            help="This column's values will be used to name your markdown files"
        )
    with col2:
        folder_col = st.selectbox(
            "Optional folder column",
            ["None"] + list(df.columns),
            help="If selected, files will be organized in folders based on this column's values"
        )

    # Properties selection
    st.markdown("### 📝 Properties")
    with st.expander("What are properties?", expanded=True):
        st.markdown("""
        Properties appear in the frontmatter (YAML section) at the top of each markdown file:
        ```yaml
        ---
        author: John Doe
        date: 2024-03-15
        category: Documentation
        ---
        ```
        Common properties include: author, date, category, status, priority
        """)

    # Regular properties
    properties_cols = st.multiselect(
        "Select columns for properties",
        df.columns,
        help="Selected columns will become key-value pairs in the frontmatter"
    )

    # List properties
    st.markdown("#### 📋 List Properties")
    with st.expander("What are list properties?", expanded=True):
        st.markdown("""
        List properties combine values into a YAML list format:
        ```yaml
        products:
          - mdf
          - ePro
          - clm
        ```
        Perfect for: products, categories, features, or any grouped items
        """)

    # List property configuration
    list_properties = []
    col1, col2 = st.columns([2, 1])
    with col1:
        list_property_name = st.text_input(
            "List property name",
            value="products",
            help="Name of the list property in the frontmatter"
        ).strip().lower()

    if list_property_name:
        list_property_cols = st.multiselect(
            f"Select columns for {list_property_name} list",
            [col for col in df.columns if col not in properties_cols],
            help="Values from these columns will be combined into a YAML list"
        )
        if list_property_cols:
            list_properties.append((list_property_name, list_property_cols))

    # Labels selection
    st.markdown("### 🏷️ Labels")
    with st.expander("What are labels?", expanded=True):
        st.markdown("""
        Labels are tags that help categorize your content. They appear as a list in the frontmatter:
        ```yaml
        labels: [python, documentation, tutorial]
        ```
        Use labels for: topics, technologies, departments, or any other categorization
        """)
    labels_cols = st.multiselect(
        "Select columns for labels",
        df.columns,
        help="Values from these columns will be combined into a labels list"
    )

    # Sections selection
    st.markdown("### 📄 Content Sections")
    with st.expander("What are sections?", expanded=True):
        st.markdown("""
        Sections become markdown headers with their content. Each selected column creates:
        ```markdown
        ## Description
        Your description text here

        ## Requirements
        Your requirements text here
        ```
        Perfect for: descriptions, requirements, notes, or any structured content
        """)
    sections_cols = st.multiselect(
        "Select columns for sections",
        df.columns,
        help="Each selected column will become a section with a header in the markdown file"
    )

    # Generate button
    st.markdown("### 🚀 Generate Files")
    if st.button("Generate Markdown Files"):
        # Create output directory and any necessary subdirectories
        os.makedirs(output_dir, exist_ok=True)

        markdown_files = {}
        file_paths = []  # Keep track of all generated file paths

        for _, row in df.iterrows():
            # Define filename and folder
            filename = f"{row[filename_col].replace(' ', '_').lower()}.md"

            # Handle folder structure
            if folder_col != "None" and not pd.isna(row[folder_col]):
                folder_name = row[folder_col].replace(" ", "_").lower()
                file_path = os.path.join(output_dir, folder_name, filename)
                os.makedirs(os.path.join(output_dir, folder_name), exist_ok=True)
            else:
                file_path = os.path.join(output_dir, filename)

            file_paths.append(file_path)

            # Build Markdown content
            md_content = "---\n"

            # Add regular properties
            for col in properties_cols:
                if col in df.columns and not pd.isna(row[col]):
                    md_content += f"{col.lower()}: {row[col]}\n"

            # Add list properties
            for prop_name, prop_cols in list_properties:
                values = []
                for col in prop_cols:
                    if not pd.isna(row[col]):
                        values.append(str(row[col]).strip())
                if values:
                    md_content += f"{prop_name}:\n"
                    for value in values:
                        md_content += f"  - {value}\n"

            # Add labels
            labels = [str(row[col]) for col in labels_cols if col in df.columns and not pd.isna(row[col])]
            if labels:
                md_content += f"labels: [{', '.join(labels)}]\n"

            md_content += "---\n\n"

            # Add sections
            for col in sections_cols:
                if col in df.columns and not pd.isna(row[col]):
                    md_content += f"## {col}\n\n{row[col]}\n\n"

            # Store file content in dictionary with full path
            markdown_files[file_path] = md_content

        # Show preview of first file
        st.markdown("### 👀 Preview")
        first_filepath, first_content = list(markdown_files.items())[0]
        st.subheader(f"Preview: {os.path.basename(first_filepath)}")
        st.code(first_content, language="markdown")

        # Display output directory information
        st.info(f"📂 Files will be generated in: {os.path.abspath(output_dir)}")

        # Create a ZIP archive for download
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for filepath, content in markdown_files.items():
                # Use relative path in ZIP file
                rel_path = os.path.relpath(filepath, output_dir)
                zipf.writestr(rel_path, content)

        zip_buffer.seek(0)
        st.download_button(
            label="⬇️ Download All Markdown Files",
            data=zip_buffer,
            file_name="markdown_files.zip",
            mime="application/zip"
        )

        st.success("✨ Markdown files generated successfully!")

        # Show file structure
        st.markdown("### 📁 Generated Files")
        file_tree = "\n".join([f"- {os.path.relpath(path, output_dir)}" for path in file_paths])
        st.code(file_tree, language="markdown")
