module.exports = {
  content: [
    './src/**/*.{html,js}',  // Tìm các tệp .html và .js trong thư mục src
    './templates/**/*.{html,js}'  // Tìm các tệp .html và .js trong thư mục templates
  ],
  theme: {
    extend: {
      width: {
        'wlogo': '420px',
        '84': '21rem',
      },
      colors: {
        brand: {
          DEFAULT: '#ff5733',  // Màu chính
          light: '#ffa599',    // Màu sáng
          dark: '#c13c27',  
          'dactrung': '#FFCB30',   // Màu tối
        },
      },
    },
  },
  plugins: [],
}
