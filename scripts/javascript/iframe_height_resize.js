function autoResize(iframe) {
          iframe.style.height = '0px';

          iframe.style.height = iframe.contentWindow.document.documentElement.scrollHeight + 'px';
      }