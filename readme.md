# 🎨 Neural Style Transfer Studio 🖼️

Transform your photos into artistic masterpieces! This application leverages the power of Neural Style Transfer to combine the content of one image with the artistic style of another, creating unique and visually stunning results. Built with Streamlit and TensorFlow, it offers an interactive and user-friendly interface for exploring the creative possibilities of AI-driven art.

## ✨ Features

* **Content Image Upload:** Easily upload the photograph you wish to transform.
* **Flexible Style Selection:**
    * Choose from a gallery of predefined artistic styles.
    * Upload your own custom style image for a personalized touch.
    * Select a single style or apply multiple styles to the content image.
* **Real-time Preview:** See your content and selected style images directly in the app.
* **Advanced Settings:**
    * Adjust output quality.
    * Experiment with preserving original image colors (experimental feature).
* **Artwork Generation:** One-click generation of styled images.
* **Progress Indication:** Visual feedback during the style transfer process.
* **Results Display:** View your generated masterpieces directly in the app.
* **Easy Download:**
    * Download individual styled images in PNG format.
    * Download all generated images conveniently as a single ZIP file.
* **Informative "About" Section:** Learn more about Neural Style Transfer and the application.
* **Responsive Design:** User-friendly interface suitable for various screen sizes.

## 🛠️ Technology Stack

* **Backend:** Python
* **Deep Learning:**
    * TensorFlow
    * TensorFlow Hub (for the Arbitrary Image Stylization model)
* **Web Framework:** Streamlit (for the interactive web interface)
* **Image Processing:** Pillow (PIL), NumPy

## ⚙️ Setup and Installation

Follow these steps to set up and run the Neural Style Transfer Studio locally:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/HackWGaveesh/Neural-Style-Transfer-Studio.git
    cd Your-Repository-Name
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    * On Windows:
        ```bash
        venv\Scripts\activate
        ```
    * On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

3.  **Install Dependencies:**
    Ensure you have the `requirements.txt` file in your project directory.
    ```bash
    pip install -r requirements.txt
    ```
    The `requirements.txt` should contain:
    ```
    streamlit==1.45.1
   tensorflow==2.18.0
   tensorflow-hub==0.16.1
   numpy==2.0.2
   pillow==11.2.1
    ```

## 📁 Directory Structure

* `StyleGan_Main.py`: The main Python script for the Streamlit application.
* `requirements.txt`: A list of Python dependencies required for the project.
* `Styles/`: This directory should contain predefined style images (e.g., `vangogh.jpg`, `monet.jpg`). The application loads styles from this folder for the "Predefined Styles" option. Make sure to populate this folder with your desired style images.
* `.gitignore` (Recommended): To exclude unnecessary files from version control.
* `README.md`: This file.

## ▶️ How to Run the Application

Once you have completed the setup and installation:

1.  Ensure your virtual environment is activated.
2.  Navigate to the project directory in your terminal.
3.  Run the Streamlit application using the following command:
    ```bash
    streamlit run StyleGan_Main.py
    ```
4.  Streamlit will typically open the application automatically in your default web browser. If not, it will display a local URL (e.g., `http://localhost:8501`) that you can open manually.

## 🚀 Usage

1.  **Upload Content Image:** In the "📸 Upload & Create" tab, use the file uploader under "📤 Content Image" to select the photo you want to style.
2.  **Select Style:**
    * **Predefined Styles:** Choose "🎨 Predefined Styles". You can opt for "Single Style" or "Multiple Styles" selection mode. Click on the style images from the gallery to select/deselect them.
    * **Custom Style:** Choose "🖌️ Custom Style" and upload your own style image.
3.  **Advanced Settings (Optional):** Expand the "⚙️ Advanced Settings" section to adjust output quality or try preserving original colors.
4.  **Generate Artwork:** Once a content image and at least one style are selected, click the "🖌️ Generate Artwork" button.
5.  **View and Download:** After processing, your styled images will appear in the "✨ Your Masterpieces" section. You can download individual images or all images as a ZIP file.

## 📝 Notes

* For optimal results, use high-quality content and style images.
* Processing time can vary depending on the size and complexity of the images, as well as your system's performance.
* The "Preserve Original Colors" feature is experimental and results may vary.

---

Happy Styling! ✨
