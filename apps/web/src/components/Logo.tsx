export default function Logo({ size = 30 }: { size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      fill="none"
      aria-hidden="true"
      className="shrink-0"
    >
      <rect width="32" height="32" rx="7" fill="#121823" stroke="#243043" />
      <path
        d="M9 7c0 6 14 12 14 18M23 7c0 6-14 12-14 18"
        stroke="#00E599"
        strokeWidth="2.2"
        strokeLinecap="round"
      />
      <circle cx="11.5" cy="11" r="1.5" fill="#22D3EE" />
      <circle cx="20.5" cy="21" r="1.5" fill="#FBBF24" />
      <circle cx="20.5" cy="11" r="1.5" fill="#3DDC84" />
      <circle cx="11.5" cy="21" r="1.5" fill="#F87171" />
    </svg>
  );
}
