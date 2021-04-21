VERSION="$1"
perl -pi -e "s/version = .*/version = $VERSION/" setup.cfg
python setup.py sdist bdist_wheel
python -m twine check dist/*
python -m twine upload dist/*
git add setup.cfg
git commit -m "Bump version $VERSION"
git tag $VERSION
git push
git push --tags
