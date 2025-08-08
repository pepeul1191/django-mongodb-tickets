class FileUpload {
  constructor(options = {}) {
    this.label = options.label || "Seleccionar imagen";
    this.acceptedFormats = options.acceptedFormats || ["jpg", "jpeg", "png"];
    this.maxSizeMB = options.maxSizeMB || 2;
    this.url = options.url || "/api/upload";
    this.fileKey = options.fileKey || "file";
    this.extraParams = options.extraParams || {};
    this.jwt = options.jwt || "";
    this.onSuccess = options.onSuccess || ((response) => console.log("Upload success:", response));
    this.onError = options.onError || ((error) => console.error("Upload error:", error));
    
    this.file = null;
    this.isLoading = false;
    
    this.initElements();
    this.setupEventListeners();
    this.updateUI();
  }
  
  initElements() {
    this.container = document.getElementById('fileUploadContainer');
    this.fileInput = document.getElementById('imageFile');
    this.uploadButton = document.getElementById('uploadButton');
    this.errorMessage = document.getElementById('errorMessage');
    this.successMessage = document.getElementById('successMessage');
    this.labelElement = this.container.querySelector('.form-label');
    
    // Update initial values
    this.labelElement.textContent = this.label;
    this.fileInput.accept = this.acceptedFormats.map(f => `.${f}`).join(',');
    this.container.querySelector('.text-muted').textContent = 
      `Formatos aceptados: ${this.acceptedFormats.join(", ").toUpperCase()} (Máx. ${this.maxSizeMB}MB)`;
  }
  
  setupEventListeners() {
    this.fileInput.addEventListener('change', this.handleFileChange.bind(this));
    this.uploadButton.addEventListener('click', this.uploadFile.bind(this));
  }
  
  handleFileChange(event) {
    const selectedFile = event.target.files[0];
    if (!selectedFile) return;

    // Validate format
    const fileExt = selectedFile.name.split('.').pop().toLowerCase();
    if (!this.acceptedFormats.includes(fileExt)) {
      this.showError(`Formato no válido. Use: ${this.acceptedFormats.join(", ").toUpperCase()}`);
      return;
    }

    // Validate size
    if (selectedFile.size > this.maxSizeMB * 1024 * 1024) {
      this.showError(`El archivo excede el tamaño máximo de ${this.maxSizeMB}MB`);
      return;
    }

    this.clearMessages();
    this.file = selectedFile;
    this.updateUI();
  }
  
  async uploadFile() {
    if (!this.file) {
      this.showError("Por favor seleccione un archivo");
      return;
    }

    this.isLoading = true;
    this.clearMessages();
    this.updateUI();

    const formData = new FormData();
    formData.append(this.fileKey, this.file);

    // Add extra parameters
    Object.keys(this.extraParams).forEach(key => {
      formData.append(key, this.extraParams[key]);
    });

    try {
      const response = await fetch(this.url, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${this.jwt}`
        },
        body: formData
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Error al subir el archivo");
      }

      this.showSuccess("Archivo subido correctamente");
      this.onSuccess(data);
    } catch (error) {
      this.showError(error.message);
      this.onError(error);
    } finally {
      this.isLoading = false;
      this.updateUI();
    }
  }
  
  showError(message) {
    this.errorMessage.textContent = message;
    this.successMessage.textContent = "";
  }
  
  showSuccess(message) {
    this.successMessage.textContent = message;
    this.errorMessage.textContent = "";
  }
  
  clearMessages() {
    this.errorMessage.textContent = "";
    this.successMessage.textContent = "";
  }
  
  updateUI() {
    // Update button state
    this.uploadButton.disabled = this.isLoading || !this.file;
    
    // Update button text and icon
    const icon = this.uploadButton.querySelector('i');
    const textNode = this.uploadButton.childNodes[2]; // Text node after icon
    
    if (this.isLoading) {
      icon.className = "fas fa-spinner spinner";
      textNode.nodeValue = " Subiendo...";
    } else {
      icon.className = "fas fa-upload";
      textNode.nodeValue = " Subir";
    }
    
    // Update input state
    this.fileInput.disabled = this.isLoading;
  }
}