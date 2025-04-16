/**
 * * This is the Keystatic configuration file. It is used to define the collections and fields that will be used in the Keystatic CMS.
 *
 * ! This works in conjunction with Astro content collections. If you update one, you must update the other.
 *
 * Access keystatic interface at /admin or /keystatic
 * This works in local mode in dev, then cloud mode in prod
 * Cloud deployment is free to sign up (up to 3 users per team)
 * Docs: https://keystatic.com/docs/cloud
 * Create a Keystatic Cloud account here: https://keystatic.cloud/
 */

import { config } from "@keystatic/core";

// components
import Collections from "@components/KeystaticComponents/Collections";

export default config({
	// Use local storage for both dev and production
	storage: { kind: "local" },
	ui: {
		brand: { name: "Colliery Software" },
	},
	collections: {
		blogEN: Collections.Blog("en"),

		// for now there is a limitation with keystatic where relationship fields don't work well with i18n features
		// If you need multiple languages here (you might not) just create multiple variants of the same author
		// this might look like "author-1-en" and "author-1-fr"
		authors: Collections.Authors(""),

		servicesEN: Collections.Services("en"),

		otherPagesEN: Collections.OtherPages("en"),
	},
});
