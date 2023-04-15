function showLoadingSpinner() {
  document.getElementById("loading-spinner2").style.display = "block";
}

const inputFile = document.getElementById("imageFile");
inputFile.addEventListener("change", function () {
  const fileNameContainer = document.getElementById("file-name-container");

  // Displaying the file name and size
  fileNameContainer.textContent = `${this.files[0].name} (${(
    this.files[0].size / 1024
  ).toFixed(2)} KB)`;
});
