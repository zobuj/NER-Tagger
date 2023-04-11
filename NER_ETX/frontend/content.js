chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'scrape') {
      const paragraphs = Array.from(document.getElementsByTagName('p')).map(
        (p) => p.innerText
      );
      console.log('Extracted paragraphs:', paragraphs);
      const formData = new URLSearchParams();
      paragraphs.forEach((paragraph, index) => {
        formData.append(`paragraphs[${index}]`, paragraph);
      });
  
      fetch('http://127.0.0.1:8000/ner/ner/process_paragraphs/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString(),
      })
        .then((response) => response.json())
        .then((data) => {
            console.log('Received data:', data);
          const modifiedParagraphs = data.modified_paragraphs;
          document.querySelectorAll('p').forEach((p, i) => {
            p.innerText = modifiedParagraphs[i];
          });
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    }
  });
  