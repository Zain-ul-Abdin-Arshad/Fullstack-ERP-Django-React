/**
 * Loading Spinner Component
 */

const Loading = ({ size = 'md', text = 'Loading...' }) => {
  const sizes = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
  };

  return (
    <div className="flex flex-col items-center justify-center p-8">
      <div className={`${sizes[size]} animate-spin rounded-full border-4 border-gray-200 border-t-primary-600`}></div>
      {text && <p className="mt-4 text-gray-600">{text}</p>}
    </div>
  );
};

export default Loading;
