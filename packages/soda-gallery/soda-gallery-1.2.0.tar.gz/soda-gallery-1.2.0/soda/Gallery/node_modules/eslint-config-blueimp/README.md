# eslint-config-blueimp

> [ESLint](https://eslint.org/) config for [blueimp](https://github.com/blueimp)
> projects.

## Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Author](#author)

## Installation

Install `eslint-config-blueimp` and save it as development dependency:

```sh
npm install --save-dev eslint-config-blueimp
```

## Usage

Add `eslint-config-blueimp` to the `extends` array in your `.eslintrc.*` file:

```js
module.exports = {
  extends: ['blueimp']
}
```

Please note that the `eslint-config-` prefix can be omitted, since it is
automatically assumed by ESLint.

## License

Released under the [MIT license](https://opensource.org/licenses/MIT).

## Author

[Sebastian Tschan](https://blueimp.net/)
