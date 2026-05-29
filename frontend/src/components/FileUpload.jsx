import { useDropzone } from 'react-dropzone';
import { DocumentIcon, XMarkIcon } from '@heroicons/react/24/outline';

const FileUpload = ({ onFileSelect, selectedFile, label, accept }) => {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: accept || {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    multiple: false,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        onFileSelect(acceptedFiles[0]);
      }
    }
  });

  const removeFile = (e) => {
    e.stopPropagation();
    onFileSelect(null);
  };

  return (
    <div className="w-full">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {label}
      </label>
      
      <div
        {...getRootProps()}
        className={`relative border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors
          ${isDragActive 
            ? 'border-blue-400 bg-blue-50' 
            : selectedFile 
              ? 'border-green-400 bg-green-50' 
              : 'border-gray-300 hover:border-gray-400'
          }`}
      >
        <input {...getInputProps()} />
        
        {selectedFile ? (
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <DocumentIcon className="h-8 w-8 text-green-600" />
              <div className="text-left">
                <p className="text-sm font-medium text-gray-900">{selectedFile.name}</p>
                <p className="text-xs text-gray-500">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
            <button
              onClick={removeFile}
              className="p-1 hover:bg-red-100 rounded-full transition-colors"
            >
              <XMarkIcon className="h-5 w-5 text-red-600" />
            </button>
          </div>
        ) : (
          <div>
            <DocumentIcon className="mx-auto h-12 w-12 text-gray-400" />
            <div className="mt-4">
              <p className="text-sm text-gray-600">
                {isDragActive ? 'Drop the file here' : 'Drag & drop a file here, or click to select'}
              </p>
              <p className="text-xs text-gray-500 mt-1">
                Supports PDF, DOCX, TXT files
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;