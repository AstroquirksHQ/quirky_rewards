module.exports = {
  plugins: [require.resolve("@trivago/prettier-plugin-sort-imports")],
  printWidth: 100,
  trailingComma: "all",
  importOrder: ["<THIRD_PARTY_MODULES>", "^@/(.*)$", "^[./]"],
  importOrderSeparation: true,
  importOrderSortSpecifiers: true,
};
