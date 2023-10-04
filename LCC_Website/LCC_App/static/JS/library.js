function showBookInfo(title, subtitle, author, year, edition, pages, pdfUrl,bookPk) {
  
  // Populate modal content with book information
  document.getElementById('bookTitle').textContent = title;
  document.getElementById('bookSubtitle').textContent = subtitle;
  document.getElementById('bookAuthor').textContent = author;
  document.getElementById('bookYear').textContent = year;
  document.getElementById('bookEdition').textContent = edition;
  document.getElementById('bookPages').textContent = pages;

  //      // Load and display PDF preview
     var pdfViewerContainer = document.getElementById('pdfViewer');
     pdfjsLib.getDocument(pdfUrl).promise.then(function(pdfDocument) {
       pdfDocument.getPage(1).then(function(page) {
         var canvas = document.createElement('canvas');
         var viewport = page.getViewport({ scale: 0.5 });
         canvas.width = viewport.width;
         canvas.height = viewport.height;
         pdfViewerContainer.innerHTML = '';
         pdfViewerContainer.appendChild(canvas);
   
         var context = canvas.getContext('2d');
         var renderContext = {
           canvasContext: context,
           viewport: viewport
         };
         page.render(renderContext);
       });
     });
  // Show the modal
  $('#bookModal').modal('show');

    
 
  // Add an event listener to the "Read PDF" button within the modal
  const readPdfButton = document.getElementById('readPdfButton');
  readPdfButton.addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default link behavior
    
    handleReadPdfButtonClick(bookPk);
    
 });
}


 // Function to handle the "Read PDF" button click
 function handleReadPdfButtonClick(thebookPk) {
  // Check if the user is authenticated (you may need to adjust the condition)
  var isAuthenticated = document.getElementById("auth-status").getAttribute("data-is-authenticated");
  isAuthenticated = isAuthenticated === "true";
  
  if (!isAuthenticated) {
    // User is not authenticated, show the "Unauthorized Access" modal
    $('#unauthorizedModal').modal('show');
  } else {
    // User is authenticated, create the PDF URL dynamically with the book's primary key
    const pdfUrl = './view_pdf/' + thebookPk + '/';

    // Set the data-pdf-url attribute with the dynamically generated PDF URL
    readPdfButton.setAttribute('data-pdf-url', pdfUrl);
    // Create and append the iframe to the container
    var pdfIframeContainer = document.getElementById('pdfIframeContainer');
    var pdfIframe = document.createElement('iframe');
    pdfIframe.src = pdfUrl;
    pdfIframe.width = '100%';
    pdfIframe.height = '500';
    pdfIframe.frameBorder = '0';
    // Add the sandbox attribute to the iframe to disable downloads
    // pdfIframe.sandbox = 'allow-same-origin allow-scripts allow-popups allow-forms allow-top-navigation allow-downloads=false';
    pdfIframeContainer.innerHTML = '';
    pdfIframeContainer.appendChild(pdfIframe);
  }
}

function toggleLibrary(bookPk, buttonElement) {
  // Check if the user is authenticated (you may need to adjust the condition)
  var isAuthenticated = document.getElementById("auth-status").getAttribute("data-is-authenticated");
  isAuthenticated = isAuthenticated === "true";
  console.log('Work properly');
  if (!isAuthenticated) {
    // User is not authenticated, show the "Unauthorized Access" modal or redirect to the login page.
    // You can implement this logic according to your requirements.
    $('#unauthorizedModal').modal('show');
    return;
  }

  // Obtain the CSRF token from the page
  var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;

  // Send an AJAX POST request to add or remove the book from the library
  $.ajax({
    url: '/add_to_library/' + bookPk + '/',
    type: 'POST',
    data: { csrfmiddlewaretoken: csrfToken }, // Include the CSRF token
    success: function (response) {
      console.log(response);
      // Update the button's icon based on the response
      if ($(buttonElement).find('i').hasClass('far')) {
        // Book was added to the library
        $(buttonElement).find('i').removeClass('far').addClass('fas');
      } else {
        // Book was removed from the library
        $(buttonElement).find('i').removeClass('fas').addClass('far');
      }

      // Show a success message (you can modify this part as needed)
      alert(response.message);
      console.log('Success and ajax worked');
    },
    error: function (error) {
      // Handle errors here, e.g., show an error message to the user.
      alert('An error occurred: ' + error.responseText);
      console.log(error);
    },
  });
}


