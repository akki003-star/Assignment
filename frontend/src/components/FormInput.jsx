function FormInput({
  label,
  name,
  type = "text",
  value,
  onChange,
  placeholder,
  required = false,
}) {
  const input = (
    <input
      name={name}
      type={type}
      required={required}
      className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
      placeholder={placeholder}
      value={value}
      onChange={onChange}
    />
  );

  if (!label) return input;

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700">{label}</label>
      {input}
    </div>
  );
}

export default FormInput;
