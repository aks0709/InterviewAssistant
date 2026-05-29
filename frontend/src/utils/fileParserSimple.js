export const parseFile = async (file) => {
  const fileType = file.type;
  
  if (fileType === 'text/plain') {
    return await file.text();
  } else {
    // For non-text files, just return the filename as placeholder
    return `File: ${file.name}\nContent: Please paste the text content manually for now.`;
  }
};