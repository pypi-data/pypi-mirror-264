function onRender(event) {
  if (!window.rendered) {
    const { label, url, disabled } = event.detail.args;
    const { theme } = event.detail;
    const isDarkMode = theme?.base === 'dark';
    // Set styles based on the theme
    const backgroundColor = isDarkMode ? 'rgb(14,17,23)' : 'white'; // Example colors for dark and light themes
    const textColor = isDarkMode ? 'rgb(250, 250, 250)' : 'rgb(0, 0, 0)';
    document.body.style.backgroundColor = backgroundColor;
    document.body.style.color = textColor;
  
    const rootElement = document.getElementById("root");
    rootElement.innerHTML = ''; // Clear any existing content

    const button = document.createElement("button");
    button.textContent = label;
    button.disabled = disabled;

    // Styling to mimic Streamlit buttons
    button.style.display = "inline-flex";
    button.style.alignItems = "center";
    button.style.justifyContent = "center";
    button.style.fontWeight = "400";
    button.style.padding = "0.25rem 0.75rem";
    button.style.borderRadius = "0.5rem";
    button.style.minHeight = "38.4px";
    button.style.margin = "0px";
    button.style.lineHeight = "1.6";
    button.style.textDecoration = "none";
    button.style.width = "auto";
    button.style.userSelect = "none";
    button.style.backgroundColor = "rgb(255, 75, 75)"; // Adjust the color as needed
    button.style.color = "rgb(255, 255, 255)";
    button.style.border = "1px solid rgb(255, 75, 75)";

    button.addEventListener("click", function() {
      window.open(url, "_blank");
      
      var timestamp = new Date().toISOString(); 
      // Add this line to send the event to Google Analytics
      // Replace 'event_name', 'event_category', and 'event_label' with your desired values
      gtag('event', 'link_button_click', {
        'event_category': 'Link Button',
        'event_label': label,
        'event_timestamp': timestamp,
      });
    });
    
    button.addEventListener("mouseenter", function() {
      setHoverButtonStyles(button);
    });
    
    button.addEventListener("mouseleave", function() {
      setDefaultButtonStyles(button);
    });

    rootElement.appendChild(button);

    window.rendered = true; // Set the flag to prevent re-initialization
  }

  // Always update the frame height in case of dynamic content changes
  Streamlit.setFrameHeight(55);
}

function setDefaultButtonStyles(button) {
    button.style.backgroundColor = "rgb(255, 75, 75)"; // Adjust the color as needed
    button.style.border = "1px solid rgb(255, 75, 75)";
  // Include other styles as previously defined
}

// Hover button styles
function setHoverButtonStyles(button) {
  button.style.backgroundColor = "rgb(255, 51, 51)"; // Lightened color for hover
  button.style.border = "1px solid rgb(255, 51, 51)";
  // Adjust other properties if needed, such as border color
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
Streamlit.setComponentReady();