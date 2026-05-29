import * as pdfjsLib from 'pdfjs-dist';
import mammoth from 'mammoth';

// Use local worker
pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url
).toString();

export const parseFile = async (file) => {
  const fileType = file.type;
  
  if (fileType === 'application/pdf') {
    return await parsePDF(file);
  } else if (fileType === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
    return await parseDOCX(file);
  } else if (fileType === 'text/plain') {
    return await parseText(file);
  } else {
    throw new Error('Unsupported file type. Please upload PDF, DOCX, or TXT files.');
  }
};

const parsePDF = async (file) => {
  const arrayBuffer = await file.arrayBuffer();
  const pdf = await pdfjsLib.getDocument(arrayBuffer).promise;
  let text = '';
  
  for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const textContent = await page.getTextContent();
    const pageText = textContent.items.map(item => item.str).join(' ');
    text += pageText + ' ';
  }
  
  return text.trim();
};

const parseDOCX = async (file) => {
  const arrayBuffer = await file.arrayBuffer();
  const result = await mammoth.extractRawText({ arrayBuffer });
  return result.value;
};

const parseText = async (file) => {
  return await file.text();
};