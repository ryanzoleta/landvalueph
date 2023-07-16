export function formatAmountToCurrency(amount: number, currencySymbol?: string): string {
  const userLang = navigator.language ?? 'en-US';
  const currencyNumber = new Intl.NumberFormat(userLang, {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount);

  if (currencySymbol) {
    return `${currencySymbol} ${currencyNumber}`;
  }
  return `${currencyNumber}`;
}

export function formatCurrency(number) {
  if (isNaN(number)) {
    return 'Invalid Number';
  }

  if (number >= 1000000) {
    return '₱' + (number / 1000000).toFixed(0) + 'M';
  } else if (number >= 1000) {
    return '₱' + (number / 1000).toFixed(0) + 'K';
  } else {
    return '₱' + number.toFixed(0);
  }
}
