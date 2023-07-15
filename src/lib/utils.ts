export function formatAmountToCurrency(amount: number, currencySymbol?: string): string {
  const userLang = navigator.language ?? 'en-US';
  const currencyNumber = new Intl.NumberFormat(userLang, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount);

  if (currencySymbol) {
    return `${currencySymbol} ${currencyNumber}`;
  }
  return `${currencyNumber}`;
}
